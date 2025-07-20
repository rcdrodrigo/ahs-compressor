# encoder.py -- versión 2.0 (con libCST)

import libcst as cst
import json
from typing import List, Dict, Union

class AHSVisitor(cst.CSTVisitor):
    """
    Recorre el CST y genera una estructura jerárquica (AHS) y un mapa de código.
    """
    def __init__(self):
        self.ahs_structure: List[Dict[str, Union[str, List]]] = []
        self.code_map: Dict[str, str] = {}
        self.node_counter = 0
        self.current_path = []

    def _get_new_ref(self) -> str:
        ref = f"@{self.node_counter}"
        self.node_counter += 1
        return ref

    def _add_node_to_structure(self, node_data: Dict):
        target = self.ahs_structure
        for key in self.current_path:
            # Navegar hasta el último diccionario de la lista de 'children'
            target = target[-1]['children']
        target.append(node_data)

    def _process_node(self, node: cst.CSTNode, node_type: str, name: str = None):
        ref = self._get_new_ref()
        self.code_map[ref] = self.module.code_for_node(node)

        node_data = {"type": node_type, "ref": ref}
        if name:
            node_data["name"] = name
        
        # Si el nodo puede tener hijos, añadir la lista
        if isinstance(node, (cst.FunctionDef, cst.ClassDef, cst.With, cst.For, cst.If)):
             node_data["children"] = []

        self._add_node_to_structure(node_data)
        
        # Añadir el ref a la ruta para anidar los hijos
        if "children" in node_data:
            self.current_path.append(ref)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> bool:
        self._process_node(node, "FunctionDef", name=node.name.value)
        return True # Continuar visitando hijos

    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        self._process_node(node, "ClassDef", name=node.name.value)
        return True

    def visit_Import(self, node: cst.Import) -> bool:
        self._process_node(node, "Import")
        return False # No visitar hijos de imports

    def visit_ImportFrom(self, node: cst.ImportFrom) -> bool:
        self._process_node(node, "ImportFrom")
        return False

    def visit_Assign(self, node: cst.Assign) -> bool:
        # Solo asignaciones a nivel de módulo/clase
        if not self.current_path or self.ahs_structure[-1]['type'] == 'ClassDef':
             self._process_node(node, "Assign")
        return False

    def leave_FunctionDef(self, original_node: cst.FunctionDef) -> None:
        self.current_path.pop()

    def leave_ClassDef(self, original_node: cst.ClassDef) -> None:
        self.current_path.pop()

    def encode(self, source_code: str) -> tuple[str, str]:
        self.module = cst.parse_module(source_code)
        self.module.visit(self)
        
        ahs_json = json.dumps(self.ahs_structure, indent=2)
        map_json = json.dumps(self.code_map, indent=2)
        
        return ahs_json, map_json

def encode_python(source: str) -> dict:
    """
    Función helper para codificar código Python a AHS v2.
    """
    encoder = AHSVisitor()
    ahs, mapping = encoder.encode(source)
    return {"ahs": ahs, "map": mapping}
