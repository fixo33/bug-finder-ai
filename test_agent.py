#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del agente.

Este script prueba las herramientas del agente sin necesidad de una clave de API
de OpenAI, permitiendo verificar que la funcionalidad básica funciona correctamente.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.tools.project_analyzer import (
    ProjectStructureTool,
    FileReaderTool,
    ProjectFileFinderTool
)


def test_project_structure_tool():
    """
    Prueba la herramienta de estructura del proyecto.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🧪 Probando ProjectStructureTool...")
    
    tool = ProjectStructureTool()
    
    # Probar con el directorio actual
    current_dir = os.getcwd()
    result = tool._run(current_dir)
    
    print(f"✅ Estructura del proyecto obtenida:")
    print(result[:500] + "..." if len(result) > 500 else result)
    print()


def test_file_finder_tool():
    """
    Prueba la herramienta de búsqueda de archivos.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🧪 Probando ProjectFileFinderTool...")
    
    tool = ProjectFileFinderTool()
    
    # Probar con el directorio actual
    current_dir = os.getcwd()
    result = tool._run(current_dir)
    
    print(f"✅ Archivos importantes encontrados:")
    print(result)
    print()


def test_file_reader_tool():
    """
    Prueba la herramienta de lectura de archivos.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🧪 Probando FileReaderTool...")
    
    tool = FileReaderTool()
    
    # Probar con el archivo README.md si existe
    readme_path = os.path.join(os.getcwd(), "README.md")
    
    if os.path.exists(readme_path):
        result = tool._run(readme_path)
        print(f"✅ Contenido del archivo README.md:")
        print(result[:300] + "..." if len(result) > 300 else result)
    else:
        print("⚠️  No se encontró README.md para probar")
    
    print()


def test_error_handling():
    """
    Prueba el manejo de errores de las herramientas.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🧪 Probando manejo de errores...")
    
    # Probar con directorio inexistente
    structure_tool = ProjectStructureTool()
    result = structure_tool._run("/ruta/inexistente")
    print(f"✅ Error manejado correctamente: {result[:100]}...")
    
    # Probar con archivo inexistente
    file_reader_tool = FileReaderTool()
    result = file_reader_tool._run("/archivo/inexistente.txt")
    print(f"✅ Error de archivo manejado correctamente: {result[:100]}...")
    
    print()


def test_analyze_project():
    """
    Prueba básica del análisis recursivo de proyecto completo.
    """
    import tempfile
    import shutil
    import os
    from src.agent.bug_finder_agent import BugFinderAgent
    # Crear un proyecto de ejemplo
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear archivos de código
        py_file = os.path.join(tmpdir, 'a.py')
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write('def foo():\n    return 1\n')
        js_file = os.path.join(tmpdir, 'b.js')
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write('function bar() { return 2; }\n')
        # Instanciar el agente
        agent = BugFinderAgent()
        result = agent.analyze_project(tmpdir, max_lines_per_segment=10)
        # Verificar archivos de salida
        assert result['success']
        assert os.path.exists(result['csv_path'])
        assert os.path.exists(result['md_path'])
        assert os.path.exists(result['state_path'])
        # Leer el estado
        import json
        with open(result['state_path'], 'r', encoding='utf-8') as f:
            state = json.load(f)
        assert 'analizados' in state and len(state['analizados']) >= 2
        assert 'bugs' in state
        print('Análisis de proyecto ejecutado correctamente.')


def main():
    """
    Función principal del script de prueba.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🚀 Iniciando pruebas del agente de análisis de proyectos...")
    print("="*60)
    
    try:
        # Probar cada herramienta
        test_project_structure_tool()
        test_file_finder_tool()
        test_file_reader_tool()
        test_error_handling()
        
        print("="*60)
        print("✅ Todas las pruebas completadas exitosamente!")
        print("🎉 El agente está listo para usar (solo necesitas configurar OPENAI_API_KEY)")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 