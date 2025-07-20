# ejemplo_uso_completo.py -- versión 2.0
"""
Ejemplo completo de uso del sistema AHS-Compressor v2 con libCST.
Demuestra la preservación de formato y la nueva estructura AHS.
"""

import json
import sys
from pathlib import Path

# Añadir módulos al path
sys.path.insert(0, str(Path(__file__).parent))

from encoder import encode_python
from decoder import decode_ahs, validate_roundtrip

def demo_preservacion_formato():
    """Demuestra que libCST preserva comentarios y formato."""
    print("🚀 Demo de preservación de formato con libCST")
    print("=" * 60)
    
    # Código de ejemplo con comentarios y formato específico
    codigo_original = '''# Este es un comentario de módulo
import math

class MathHelper:
    """Una clase para ayudar con cálculos matemáticos."""
    
    # Una constante importante
    EULER_CONSTANT = 0.57721

    def calculate_circle_area(self, radius: float) -> float:
        """Calcula el área de un círculo, con un comentario dentro."""
        # La fórmula es pi * r^2
        return math.pi * (radius ** 2)


# Código fuera de cualquier clase
def standalone_function():
    print("Esta función está sola.")
'''
    
    print("📝 Código Original (con comentarios y formato):")
    print(codigo_original)
    print("-" * 30)
    
    # Paso 1: Codificar
    print("🔄 Codificando a formato AHS (JSON)...")
    result = encode_python(codigo_original)
    ahs_json = result["ahs"]
    map_json = result["map"]
    
    print("📊 AHS (JSON):")
    print(ahs_json)
    print("\n📋 Mapa de Código (JSON):")
    print(map_json)
    print("-" * 30)
    
    # Métricas
    original_size = len(codigo_original)
    # El tamaño "comprimido" es la suma del AHS y el mapa
    compressed_size = len(ahs_json) + len(map_json)
    ratio = compressed_size / original_size if original_size > 0 else 0
    
    print("📈 Métricas de \"compresión\":")
    print(f"   Tamaño original: {original_size} bytes")
    print(f"   Tamaño AHS+Mapa: {compressed_size} bytes")
    print(f"   Ratio: {ratio:.2%}")
    print("-" * 30)
    
    # Paso 2: Decodificar
    print("🔄 Decodificando de AHS...")
    codigo_decodificado = decode_ahs(ahs_json, map_json)
    
    print("📝 Código Decodificado:")
    print(codigo_decodificado)
    print("-" * 30)
    
    # Paso 3: Validar
    print("✅ Validando round-trip (debe ser 100% idéntico)...")
    es_valido = validate_roundtrip(codigo_original, codigo_decodificado)
    print(f"   Resultado: {'✅ VÁLIDO' if es_valido else '❌ INVÁLIDO'}")
    
    if not es_valido:
        print("\n--- DIFERENCIAS ---")
        import difflib
        diff = difflib.unified_diff(
            codigo_original.splitlines(keepends=True),
            codigo_decodificado.splitlines(keepends=True),
            fromfile='original', tofile='decodificado',
        )
        print(''.join(diff))

def main():
    """Función principal que ejecuta la demo."""
    print("🎯 Sistema AHS-Compressor v2 - Demostración con libCST")
    print("========================================================")
    print("Autor: Rodrigo | Versión: 2.0")
    print()
    
    try:
        demo_preservacion_formato()
        
        print("\n🎉 ¡Demostración completada!")
        print("\n📚 Próximos pasos:")
        print("   1. Explorar el nuevo formato AHS en JSON.")
        print("   2. Verificar cómo los comentarios y espacios se preservan en el mapa.")
        print("   3. Implementar la Fase 2: Soporte para proyectos completos.")
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
