"""
Ejemplo de uso del análisis de proyectos completos.

Este script demuestra cómo usar el método analyze_project del BugFinderAgent
para analizar un proyecto completo, con diferentes configuraciones y opciones.
"""

import os
import sys
from src.agent.bug_finder_agent import BugFinderAgent


def analyze_current_project():
    """
    Analiza el proyecto actual (langgraph-agent) como ejemplo.
    """
    print("🔍 Analizando el proyecto actual...")
    
    # Obtener la ruta del proyecto actual
    current_dir = os.getcwd()
    
    # Configurar rutas de salida
    state_file = os.path.join(current_dir, "bug_analysis_state.json")
    csv_file = os.path.join(current_dir, "bug_analysis_results.csv")
    md_file = os.path.join(current_dir, "bug_analysis_report.md")
    
    # Crear instancia del agente
    agent = BugFinderAgent(
        model_name="gemini-2.0-flash",
        model_provider="google_genai",
        temperature=0.1
    )
    
    try:
        # Ejecutar análisis
        result = agent.analyze_project(
            project_path=current_dir,
            state_path=state_file,
            csv_path=csv_file,
            md_path=md_file,
            max_lines_per_segment=200
        )
        
        # Mostrar resultados
        print("\n📊 Resultados del análisis:")
        print(f"   ✅ Proyecto: {result['proyecto']}")
        print(f"   🐛 Total de bugs: {result['total_bugs']}")
        print(f"   🔴 Alta severidad: {result['alta']}")
        print(f"   🟡 Media severidad: {result['media']}")
        print(f"   🟢 Baja severidad: {result['baja']}")
        print(f"\n📁 Archivos generados:")
        print(f"   📄 Estado: {result['state_path']}")
        print(f"   📊 Bugs CSV: {result['csv_path']}")
        print(f"   📋 Reporte MD: {result['md_path']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        return None


def analyze_specific_project(project_path: str):
    """
    Analiza un proyecto específico.
    
    @param project_path Ruta al proyecto a analizar
    """
    if not os.path.exists(project_path):
        print(f"❌ El directorio {project_path} no existe")
        return None
    
    print(f"🔍 Analizando proyecto: {project_path}")
    
    # Crear instancia del agente
    agent = BugFinderAgent()
    
    try:
        # Ejecutar análisis
        result = agent.analyze_project(
            project_path=project_path,
            max_lines_per_segment=150
        )
        
        # Mostrar resultados
        print(f"\n📊 Resultados del análisis de {result['proyecto']}:")
        print(f"   🐛 Bugs detectados: {result['total_bugs']}")
        print(f"   🔴 Alta severidad: {result['alta']}")
        print(f"   🟡 Media severidad: {result['media']}")
        print(f"   🟢 Baja severidad: {result['baja']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        return None


def resume_analysis(project_path: str):
    """
    Reanuda un análisis interrumpido.
    
    @param project_path Ruta al proyecto
    """
    state_file = os.path.join(project_path, "bug_finder_state.json")
    
    if not os.path.exists(state_file):
        print(f"❌ No se encontró archivo de estado en {state_file}")
        return None
    
    print(f"🔄 Reanudando análisis de {project_path}...")
    
    # Crear instancia del agente
    agent = BugFinderAgent()
    
    try:
        # Reanudar análisis
        result = agent.analyze_project(project_path)
        
        print(f"✅ Análisis reanudado exitosamente")
        print(f"   🐛 Bugs totales: {result['total_bugs']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error al reanudar análisis: {str(e)}")
        return None


def main():
    """
    Función principal que demuestra diferentes usos del análisis de proyectos.
    """
    print("🚀 Ejemplo de análisis de proyectos completos")
    print("=" * 50)
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--resume" and len(sys.argv) > 2:
            # Reanudar análisis
            resume_analysis(sys.argv[2])
        elif len(sys.argv) > 1:
            # Analizar proyecto específico
            analyze_specific_project(sys.argv[1])
        else:
            print("❌ Uso: python example_project_analysis.py [ruta_proyecto]")
            print("   o: python example_project_analysis.py --resume [ruta_proyecto]")
    else:
        # Analizar proyecto actual
        analyze_current_project()
    
    print("\n✨ Ejemplo completado!")


if __name__ == "__main__":
    main() 