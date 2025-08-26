"""
Ejemplo de uso del agente de detección de bugs con rutas dinámicas.

Este script demuestra cómo usar el agente para analizar diferentes archivos
especificando la ruta de forma dinámica.
"""

import os
import sys
from pathlib import Path
from src.agent import BugFinderAgent

def analyze_file_dynamically(file_path: str):
    """
    Analiza un archivo especificado dinámicamente.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @param file_path Ruta al archivo a analizar
    """
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo {file_path} no existe")
        return
    
    # Verificar que es un archivo (no un directorio)
    if not os.path.isfile(file_path):
        print(f"❌ Error: {file_path} no es un archivo válido")
        return
    
    print(f"🔍 Analizando archivo: {file_path}")
    print("=" * 60)
    
    try:
        # Crear el agente
        bug_finder = BugFinderAgent(
            model_name="gemini-2.0-flash",
            model_provider="google_genai",
            temperature=0.1
        )
        
        # Analizar el archivo
        result = bug_finder.analyze_file(file_path)
        
        if result["success"]:
            print("✅ Análisis completado exitosamente")
            print("\n" + "=" * 60)
            print("RESULTADO DEL ANÁLISIS:")
            print("=" * 60)
            print(result["analysis"])
        else:
            print("❌ Error durante el análisis:")
            print(result["error"])
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def analyze_multiple_files(file_paths: list):
    """
    Analiza múltiples archivos especificados.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @param file_paths Lista de rutas a archivos
    """
    print(f"🔍 Analizando {len(file_paths)} archivos...")
    print("=" * 60)
    
    try:
        # Crear el agente
        bug_finder = BugFinderAgent(
            model_name="gemini-2.0-flash",
            model_provider="google_genai",
            temperature=0.1
        )
        
        # Analizar múltiples archivos
        results = bug_finder.analyze_multiple_files(file_paths)
        
        for i, result in enumerate(results):
            file_path = file_paths[i]
            print(f"\n📁 Archivo {i+1}/{len(file_paths)}: {file_path}")
            print("-" * 40)
            
            if result["success"]:
                print("✅ Análisis exitoso")
                # Mostrar solo un resumen para no saturar la salida
                analysis = result["analysis"]
                lines = analysis.split('\n')
                summary_lines = [line for line in lines if 'RESUMEN' in line or 'Total de bugs' in line]
                if summary_lines:
                    print("📊 Resumen:")
                    for line in summary_lines:
                        print(f"   {line}")
                else:
                    print("📝 Análisis disponible (archivo sin bugs detectados)")
            else:
                print(f"❌ Error: {result['error']}")
                
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def find_code_files_in_directory(directory: str, extensions: list = None):
    """
    Encuentra archivos de código en un directorio.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @param directory Directorio a buscar
    @param extensions Lista de extensiones a buscar (opcional)
    @return Lista de rutas de archivos encontrados
    """
    if extensions is None:
        # Extensiones comunes de código
        extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala']
    
    code_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            # Ignorar directorios comunes que no contienen código
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', 'env', '.pytest_cache']]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in extensions:
                    code_files.append(str(file_path))
                    
    except Exception as e:
        print(f"❌ Error al buscar archivos: {str(e)}")
    
    return code_files

def main():
    """
    Función principal con ejemplos de uso.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    """
    print("🚀 EJEMPLO DE USO DEL AGENTE DE DETECCIÓN DE BUGS")
    print("=" * 60)
    print()
    
    # Ejemplo 1: Analizar un archivo específico
    print("📋 EJEMPLO 1: Analizar archivo específico")
    print("-" * 40)
    analyze_file_dynamically("test_buggy_code.py")
    print()
    
    # Ejemplo 2: Analizar múltiples archivos
    print("📋 EJEMPLO 2: Analizar múltiples archivos")
    print("-" * 40)
    files_to_analyze = [
        "test_buggy_code.py",
        "agent.py"
    ]
    analyze_multiple_files(files_to_analyze)
    print()
    
    # Ejemplo 3: Buscar archivos de código en el directorio actual
    print("📋 EJEMPLO 3: Buscar archivos de código automáticamente")
    print("-" * 40)
    current_dir = "."
    code_files = find_code_files_in_directory(current_dir)
    
    if code_files:
        print(f"📁 Encontrados {len(code_files)} archivos de código:")
        for file_path in code_files[:5]:  # Mostrar solo los primeros 5
            print(f"   - {file_path}")
        if len(code_files) > 5:
            print(f"   ... y {len(code_files) - 5} archivos más")
        
        # Preguntar si analizar todos los archivos encontrados
        print("\n¿Deseas analizar todos los archivos encontrados? (s/n): ", end="")
        response = input().lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            analyze_multiple_files(code_files)
    else:
        print("No se encontraron archivos de código en el directorio actual.")
    
    print("\n✅ Ejemplos completados")

if __name__ == "__main__":
    # Si se proporciona un argumento de línea de comandos, analizar ese archivo
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        analyze_file_dynamically(file_path)
    else:
        main() 