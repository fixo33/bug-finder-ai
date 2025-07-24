"""
Pruebas específicas para el análisis de proyectos completos.

Este módulo contiene pruebas para verificar que el método analyze_project
funciona correctamente, genera los archivos de reporte y persiste el estado.
"""

import os
import tempfile
import json
import csv
from src.agent.bug_finder_agent import BugFinderAgent


def test_project_analysis_with_files():
    """
    Prueba completa del análisis de proyecto con archivos de código reales.
    """
    print("🧪 Probando análisis completo de proyecto...")
    
    # Crear un proyecto de ejemplo con archivos que contengan bugs
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear archivo Python con bugs
        py_file = os.path.join(tmpdir, 'buggy_code.py')
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write("""
def divide_numbers(a, b):
    return a / b  # Posible división por cero

def process_list(items):
    result = []
    for i in range(len(items)):
        result.append(items[i])  # Acceso directo sin verificar índices
    return result

def main():
    x = 10
    y = 0
    result = divide_numbers(x, y)  # División por cero
    print(result)
    
    my_list = [1, 2, 3]
    processed = process_list(my_list)
    print(processed)
""")
        
        # Crear archivo JavaScript con bugs
        js_file = os.path.join(tmpdir, 'buggy_script.js')
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write("""
function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i <= items.length; i++) {  // <= debería ser <
        total += items[i];  // Acceso fuera de rango
    }
    return total;
}

function processUserInput(input) {
    // Sin validación de entrada
    return eval(input);  // Uso peligroso de eval
}

// Variables no declaradas
console.log(undefinedVariable);  // Variable no definida
""")
        
        # Instanciar el agente
        agent = BugFinderAgent()
        
        # Ejecutar análisis
        result = agent.analyze_project(tmpdir, max_lines_per_segment=50)
        
        # Verificar resultado
        assert result['success'], "El análisis debería ser exitoso"
        assert result['proyecto'] == os.path.basename(tmpdir), "El nombre del proyecto debería coincidir"
        
        # Verificar archivos generados
        assert os.path.exists(result['state_path']), "El archivo de estado debería existir"
        assert os.path.exists(result['csv_path']), "El archivo CSV debería existir"
        assert os.path.exists(result['md_path']), "El archivo MD debería existir"
        
        # Verificar contenido del estado
        with open(result['state_path'], 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        assert 'analizados' in state, "El estado debería contener archivos analizados"
        assert 'pendientes' in state, "El estado debería contener archivos pendientes"
        assert 'bugs' in state, "El estado debería contener bugs"
        
        # Verificar que se analizaron los archivos
        analizados = set(state['analizados'])
        expected_files = {py_file, js_file}
        assert expected_files.issubset(analizados), f"Deberían haberse analizado {expected_files}"
        
        # Verificar contenido del CSV
        with open(result['csv_path'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            bugs = list(reader)
        
        assert len(bugs) > 0, "Debería haber bugs detectados"
        
        # Verificar contenido del MD
        with open(result['md_path'], 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        assert "Reporte de Bugs" in md_content, "El reporte MD debería contener el título"
        assert "Resumen" in md_content, "El reporte MD debería contener resumen"
        
        print(f"✅ Análisis completado exitosamente:")
        print(f"   - Archivos analizados: {len(state['analizados'])}")
        print(f"   - Bugs detectados: {len(bugs)}")
        print(f"   - Estado guardado en: {result['state_path']}")
        print(f"   - Bugs registrados en: {result['csv_path']}")
        print(f"   - Reporte generado en: {result['md_path']}")


def test_project_analysis_resume():
    """
    Prueba la funcionalidad de reanudación del análisis.
    """
    print("🧪 Probando reanudación de análisis...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear archivos
        files = []
        for i in range(3):
            file_path = os.path.join(tmpdir, f'file_{i}.py')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"def function_{i}():\n    return {i}\n")
            files.append(file_path)
        
        agent = BugFinderAgent()
        
        # Primera ejecución (analiza solo el primer archivo)
        result1 = agent.analyze_project(tmpdir, max_lines_per_segment=10)
        
        # Verificar que se analizó al menos un archivo
        with open(result1['state_path'], 'r', encoding='utf-8') as f:
            state1 = json.load(f)
        
        assert len(state1['analizados']) > 0, "Debería haberse analizado al menos un archivo"
        
        # Segunda ejecución (debería continuar desde donde se quedó)
        result2 = agent.analyze_project(tmpdir, max_lines_per_segment=10)
        
        # Verificar que se continuó el análisis
        with open(result2['state_path'], 'r', encoding='utf-8') as f:
            state2 = json.load(f)
        
        assert len(state2['analizados']) >= len(state1['analizados']), "Debería haberse continuado el análisis"
        
        print("✅ Reanudación de análisis funcionando correctamente")


def main():
    """
    Ejecuta todas las pruebas de análisis de proyectos.
    """
    print("🚀 Iniciando pruebas de análisis de proyectos...")
    print("=" * 60)
    
    try:
        test_project_analysis_with_files()
        print()
        test_project_analysis_resume()
        print()
        print("🎉 Todas las pruebas de análisis de proyectos pasaron exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {str(e)}")
        raise


if __name__ == "__main__":
    main() 