#!/usr/bin/env python3
"""
Script de instalación automática para el agente de análisis de proyectos.

Este script automatiza el proceso de configuración del entorno virtual
y la instalación de dependencias.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Ejecuta un comando del sistema y maneja errores.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @param command Comando a ejecutar
    @param description Descripción del comando para mostrar al usuario
    @return True si el comando se ejecutó exitosamente, False en caso contrario
    """
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stdout:
            print(f"Salida: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """
    Verifica que la versión de Python sea compatible.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @return True si la versión es compatible, False en caso contrario
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Se requiere Python 3.8 o superior. Versión actual: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def create_virtual_environment():
    """
    Crea el entorno virtual de Python.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @return True si se creó exitosamente, False en caso contrario
    """
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  El entorno virtual ya existe. ¿Deseas recrearlo? (y/N): ", end="")
        response = input().strip().lower()
        if response != 'y':
            print("✅ Usando entorno virtual existente")
            return True
        else:
            print("🗑️  Eliminando entorno virtual existente...")
            import shutil
            shutil.rmtree(venv_path)
    
    return run_command("python -m venv venv", "Creando entorno virtual")


def install_dependencies():
    """
    Instala las dependencias del proyecto.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @return True si se instalaron exitosamente, False en caso contrario
    """
    # Determinar el comando de pip según el sistema operativo
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias")


def setup_environment_file():
    """
    Configura el archivo de variables de entorno.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @return True si se configuró exitosamente, False en caso contrario
    """
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("⚠️  El archivo .env ya existe")
        return True
    
    if not env_example.exists():
        print("❌ Error: No se encontró el archivo env.example")
        return False
    
    try:
        # Copiar el archivo de ejemplo
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Archivo .env creado desde env.example")
        print("📝 Recuerda editar .env y agregar tu clave de API de OpenAI")
        return True
    except Exception as e:
        print(f"❌ Error al crear .env: {e}")
        return False


def run_tests():
    """
    Ejecuta las pruebas básicas del agente.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @return True si las pruebas pasaron, False en caso contrario
    """
    print("🧪 Ejecutando pruebas básicas...")
    
    # Determinar el comando de python según el sistema operativo
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} test_agent.py", "Ejecutando pruebas")


def print_activation_instructions():
    """
    Imprime las instrucciones para activar el entorno virtual.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("\n" + "="*60)
    print("🎉 ¡Instalación completada exitosamente!")
    print("="*60)
    
    print("\n📋 Para usar el agente:")
    
    if platform.system() == "Windows":
        print("1. Activar el entorno virtual:")
        print("   venv\\Scripts\\activate")
    else:
        print("1. Activar el entorno virtual:")
        print("   source venv/bin/activate")
    
    print("\n2. Configurar la clave de API de OpenAI:")
    print("   Edita el archivo .env y agrega tu clave de API")
    
    print("\n3. Ejecutar el agente:")
    print("   python main.py /ruta/al/proyecto")
    
    print("\n4. Para más información, consulta el README.md")
    print("="*60)


def main():
    """
    Función principal del script de instalación.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    """
    print("🚀 Instalador del Agente de Análisis de Proyectos")
    print("="*60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        print("❌ Error al crear el entorno virtual")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error al instalar dependencias")
        sys.exit(1)
    
    # Configurar archivo de entorno
    if not setup_environment_file():
        print("❌ Error al configurar archivo de entorno")
        sys.exit(1)
    
    # Ejecutar pruebas
    if not run_tests():
        print("⚠️  Las pruebas fallaron, pero la instalación continuó")
    
    # Mostrar instrucciones
    print_activation_instructions()


if __name__ == "__main__":
    main() 