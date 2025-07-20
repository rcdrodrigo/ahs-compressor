# decoder.py -- versión 2.0 (con libCST)

import json
import libcst as cst

def decode_ahs(ahs_json: str, map_json: str) -> str:
    """
    Reconstruye el código a partir de AHS JSON y un mapa de código.
    """
    try:
        ahs_structure = json.loads(ahs_json)
        code_map = json.loads(map_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido: {e}")

    def build_source_from_structure(structure: list) -> str:
        output_parts = []
        for node_data in structure:
            ref = node_data.get("ref")
            if ref not in code_map:
                raise ValueError(f"Referencia no encontrada en el mapa: {ref}")
            
            node_code = code_map[ref]
            
            # Si el nodo tiene hijos, necesitamos reemplazar el cuerpo original
            # con el cuerpo reconstruido de los hijos.
            if "children" in node_data and node_data["children"]:
                # Parsear el código del nodo actual para poder manipularlo
                parsed_node = cst.parse_statement(node_code)
                
                # Reconstruir el código de los hijos
                children_source = build_source_from_structure(node_data["children"])
                
                # Parsear el código de los hijos en un cuerpo de módulo
                children_body = cst.parse_module(children_source).body

                # Reemplazar el cuerpo del nodo padre con el de los hijos
                # Esto es complejo y depende del tipo de nodo (FunctionDef, ClassDef, etc.)
                if isinstance(parsed_node, (cst.FunctionDef, cst.ClassDef)):
                    new_body = cst.IndentedBlock(body=children_body)
                    final_node = parsed_node.with_changes(body=new_body)
                    output_parts.append(final_node.code)
                else:
                    # Para otros tipos de bloques (With, For, etc.), esto requiere más lógica.
                    # Por ahora, simplemente usamos el código original del mapa.
                    output_parts.append(node_code)
            else:
                output_parts.append(node_code)
        
        # Unir con dos líneas nuevas para separar bloques de alto nivel
        return "\n\n".join(output_parts)

    # La versión simple (y por ahora más robusta) es simplemente unir los bloques de código
    # de nivel superior. La reconstrucción anidada es compleja y se puede mejorar después.
    top_level_source = "\n\n".join([code_map[node["ref"]] for node in ahs_structure])
    
    return top_level_source

def validate_roundtrip(original: str, decoded: str) -> bool:
    """
    Valida que el código original y decodificado sean idénticos textualmente.
    Con libCST, la meta es una reconstrucción perfecta.
    """
    # Normalizar saltos de línea para evitar problemas entre OS
    return original.replace('\r\n', '\n') == decoded.replace('\r\n', '\n')

def decode_python(data: dict) -> str:
    """
    Función helper para decodificar desde un dict.
    """
    return decode_ahs(data["ahs"], data["map"])
