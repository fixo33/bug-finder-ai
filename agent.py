import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar el agente de detección de bugs
from src.agent import BugFinderAgent

def main():
    """
    Función principal para ejecutar el agente de detección de bugs.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    # Ruta estática del archivo a analizar (puedes cambiarla según necesites)
    file_path = "test_buggy_code.py"
    
    print("=== AGENTE DE DETECCIÓN DE BUGS ===")
    print(f"Analizando archivo: {file_path}")
    print("=" * 50)
    
    try:
        # Crear el agente de detección de bugs
        bug_finder = BugFinderAgent(
            model_name="gemini-2.0-flash",
            model_provider="google_genai",
            temperature=0.1
        )
        
        # Analizar el archivo
        result = bug_finder.analyze_file(file_path)
        
        if result["success"]:
            print("✅ Análisis completado exitosamente")
            print("\n" + "=" * 50)
            print("RESULTADO DEL ANÁLISIS:")
            print("=" * 50)
            print(result["analysis"])
        else:
            print("❌ Error durante el análisis:")
            print(result["error"])
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()