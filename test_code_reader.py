"""
Script de prueba para la herramienta de lectura de código.

Este script demuestra cómo usar la herramienta CodeReaderTool
para leer archivos de diferentes lenguajes de programación.
"""

import os
from src.tools import CodeReaderTool

def test_code_reader():
    """
    Prueba la herramienta de lectura de código con diferentes archivos.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    """
    # Crear instancia de la herramienta
    code_reader = CodeReaderTool()
    
    # Lista de archivos de prueba (puedes agregar más)
    test_files = [
        "test_buggy_code.py",
        "agent.py",
        "main.py"
    ]
    
    print("=== PRUEBA DE HERRAMIENTA DE LECTURA DE CÓDIGO ===")
    print()
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"📁 Analizando: {file_path}")
            print("-" * 40)
            
            try:
                # Leer el archivo
                result = code_reader._run(file_path)
                
                # Mostrar solo las primeras líneas para no saturar la salida
                lines = result.split('\n')
                preview = '\n'.join(lines[:20])  # Primeras 20 líneas
                
                if len(lines) > 20:
                    preview += "\n... (archivo truncado para mostrar)"
                
                print(preview)
                print()
                
            except Exception as e:
                print(f"❌ Error al leer {file_path}: {str(e)}")
                print()
        else:
            print(f"⚠️  Archivo no encontrado: {file_path}")
            print()

def test_supported_extensions():
    """
    Muestra las extensiones de archivos soportadas.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    """
    code_reader = CodeReaderTool()
    
    print("=== EXTENSIONES DE ARCHIVOS SOPORTADAS ===")
    print()
    
    # Agrupar extensiones por categoría
    categories = {
        "Python": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext.startswith('.py')],
        "JavaScript/TypeScript": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']],
        "Java": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.java', '.class', '.jar']],
        "C/C++": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx']],
        "Web": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.html', '.htm', '.xhtml', '.css', '.scss', '.sass', '.less']],
        "Configuración": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg']],
        "Shell": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext in ['.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd']],
        "Otros": [ext for ext in code_reader.SUPPORTED_EXTENSIONS if ext not in ['.py', '.pyx', '.pyi', '.pyw', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.java', '.class', '.jar', '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.html', '.htm', '.xhtml', '.css', '.scss', '.sass', '.less', '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd']]
    }
    
    for category, extensions in categories.items():
        if extensions:
            print(f"📂 {category}:")
            print(f"   {', '.join(sorted(extensions))}")
            print()
    
    print(f"Total de extensiones soportadas: {len(code_reader.SUPPORTED_EXTENSIONS)}")

if __name__ == "__main__":
    print("🔧 PRUEBAS DE LA HERRAMIENTA DE LECTURA DE CÓDIGO")
    print("=" * 60)
    print()
    
    # Mostrar extensiones soportadas
    test_supported_extensions()
    print()
    
    # Probar lectura de archivos
    test_code_reader()
    
    print("✅ Pruebas completadas") 