#!/usr/bin/env python3
"""
Script principal para ejecutar el agente de análisis de proyectos.

Este script proporciona una interfaz de línea de comandos para analizar
la estructura de proyectos de desarrollo usando el agente de IA.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent.project_analyzer_agent import ProjectAnalyzerAgent


def setup_environment():
    """
    Configura el entorno de ejecución.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @throws SystemExit Si no se puede configurar el entorno correctamente
    """
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar que existe la clave de API de OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: No se encontró la variable de entorno OPENAI_API_KEY")
        print("Por favor, crea un archivo .env con tu clave de API:")
        print("OPENAI_API_KEY=tu_clave_aqui")
        sys.exit(1)


def validate_project_path(project_path: str) -> str:
    """
    Valida que la ruta del proyecto sea válida.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @param project_path Ruta al proyecto a validar
    @return Ruta absoluta del proyecto si es válida
    @throws SystemExit Si la ruta no es válida
    """
    # Convertir a ruta absoluta
    abs_path = os.path.abspath(project_path)
    
    # Verificar que existe
    if not os.path.exists(abs_path):
        print(f"❌ Error: El directorio '{project_path}' no existe")
        sys.exit(1)
    
    # Verificar que es un directorio
    if not os.path.isdir(abs_path):
        print(f"❌ Error: '{project_path}' no es un directorio válido")
        sys.exit(1)
    
    return abs_path


def print_analysis_results(results: dict):
    """
    Imprime los resultados del análisis de forma organizada.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    
    @param results Diccionario con los resultados del análisis
    """
    print("\n" + "="*80)
    print("📊 ANÁLISIS DEL PROYECTO")
    print("="*80)
    
    print(f"\n📍 Ruta del proyecto: {results['project_path']}")
    
    print("\n" + "-"*80)
    print("🌳 ESTRUCTURA DEL PROYECTO")
    print("-"*80)
    print(results['project_structure'])
    
    print("\n" + "-"*80)
    print("📁 ARCHIVOS IMPORTANTES")
    print("-"*80)
    print(results['important_files'])
    
    if results['file_content'] and results['file_content'] != "No se encontró ningún archivo de muestra para leer":
        print("\n" + "-"*80)
        print("📄 CONTENIDO DEL ARCHIVO MUESTRA")
        print("-"*80)
        print(results['file_content'])
    
    print("\n" + "-"*80)
    print("🤖 ANÁLISIS FINAL")
    print("-"*80)
    print(results['analysis'])
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80)


def main():
    """
    Función principal del script.
    
    @author Fabian Silva <devawsoftware@gmail.com>
    @version 1.0
    """
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description="Agente de IA para análisis de proyectos de desarrollo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py /ruta/al/proyecto
  python main.py C:\\Users\\Usuario\\Desktop\\mi-proyecto-angular
  python main.py --api-key tu_clave_aqui /ruta/al/proyecto
        """
    )
    
    parser.add_argument(
        "project_path",
        help="Ruta al directorio del proyecto a analizar"
    )
    
    parser.add_argument(
        "--api-key",
        help="Clave de API de OpenAI (opcional, puede usar variable de entorno)"
    )
    
    parser.add_argument(
        "--output",
        help="Archivo de salida para guardar los resultados (opcional)"
    )
    
    # Parsear argumentos
    args = parser.parse_args()
    
    try:
        # Configurar entorno
        setup_environment()
        
        # Validar ruta del proyecto
        project_path = validate_project_path(args.project_path)
        
        print("🚀 Iniciando agente de análisis de proyectos...")
        print(f"📂 Analizando proyecto en: {project_path}")
        
        # Crear y ejecutar el agente
        agent = ProjectAnalyzerAgent(openai_api_key=args.api_key)
        
        print("🔍 Analizando estructura del proyecto...")
        results = agent.analyze_project(project_path)
        
        # Imprimir resultados
        print_analysis_results(results)
        
        # Guardar resultados en archivo si se especifica
        if args.output:
            try:
                import json
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Resultados guardados en: {args.output}")
            except Exception as e:
                print(f"\n⚠️  Error al guardar resultados: {e}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Análisis interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 