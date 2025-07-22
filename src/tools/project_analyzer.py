"""
Herramientas para analizar la estructura de proyectos.

Este módulo contiene las herramientas que el agente de IA utiliza para
explorar y analizar la estructura de proyectos de desarrollo.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class ProjectStructureInput(BaseModel):
    """Modelo de entrada para las herramientas de análisis de proyecto."""
    
    project_path: str = Field(
        description="Ruta completa al directorio del proyecto a analizar"
    )


class FileContentInput(BaseModel):
    """Modelo de entrada para leer contenido de archivos."""
    
    file_path: str = Field(
        description="Ruta completa al archivo que se desea leer"
    )


class ProjectStructureTool(BaseTool):
    """
    Herramienta para obtener la estructura de directorios de un proyecto.
    
    Esta herramienta utiliza el comando 'tree' en sistemas Unix/Linux
    o una implementación alternativa en Windows para mostrar la
    estructura de directorios de un proyecto.
    """
    
    name: str = "project_structure"
    description: str = "Obtiene la estructura de directorios de un proyecto usando el comando tree"
    args_schema: type[BaseModel] = ProjectStructureInput
    
    def _run(self, project_path: str) -> str:
        """
        Ejecuta el comando tree para obtener la estructura del proyecto.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param project_path Ruta al directorio del proyecto
        @return Estructura de directorios en formato texto
        @throws FileNotFoundError Si el directorio del proyecto no existe
        @throws subprocess.CalledProcessError Si el comando tree falla
        """
        try:
            # Verificar que el directorio existe
            if not os.path.exists(project_path):
                raise FileNotFoundError(f"El directorio {project_path} no existe")
            
            # Intentar usar el comando tree
            try:
                result = subprocess.run(
                    ["tree", project_path, "-I", "node_modules|.git|__pycache__|*.pyc|.DS_Store"],
                    capture_output=True,
                    text=True,
                    cwd=project_path
                )
                
                if result.returncode == 0:
                    return result.stdout
                else:
                    # Si tree no está disponible, usar implementación alternativa
                    return self._generate_tree_structure(project_path)
                    
            except FileNotFoundError:
                # tree no está disponible, usar implementación alternativa
                return self._generate_tree_structure(project_path)
                
        except Exception as e:
            return f"Error al obtener la estructura del proyecto: {str(e)}"
    
    def _generate_tree_structure(self, project_path: str) -> str:
        """
        Genera una estructura de árbol alternativa cuando tree no está disponible.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param project_path Ruta al directorio del proyecto
        @return Estructura de directorios generada manualmente
        """
        structure = []
        ignored_dirs = {'.git', 'node_modules', '__pycache__', '.DS_Store', 'venv', 'env'}
        
        def build_tree(path: Path, prefix: str = "", is_last: bool = True):
            """Construye recursivamente la estructura del árbol."""
            if path.name in ignored_dirs:
                return
            
            # Agregar el directorio/archivo actual
            connector = "└── " if is_last else "├── "
            structure.append(f"{prefix}{connector}{path.name}")
            
            if path.is_dir():
                # Obtener elementos del directorio
                items = [item for item in path.iterdir() if item.name not in ignored_dirs]
                items.sort(key=lambda x: (x.is_file(), x.name.lower()))
                
                # Procesar cada elemento
                for i, item in enumerate(items):
                    is_last_item = i == len(items) - 1
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    build_tree(item, new_prefix, is_last_item)
        
        try:
            project_root = Path(project_path)
            build_tree(project_root)
            return "\n".join(structure) if structure else "Directorio vacío"
        except Exception as e:
            return f"Error al generar estructura: {str(e)}"


class FileReaderTool(BaseTool):
    """
    Herramienta para leer el contenido de archivos del proyecto.
    
    Esta herramienta permite al agente leer archivos específicos
    para analizar su contenido y estructura.
    """
    
    name: str = "file_reader"
    description: str = "Lee el contenido de un archivo específico del proyecto"
    args_schema: type[BaseModel] = FileContentInput
    
    def _run(self, file_path: str) -> str:
        """
        Lee el contenido de un archivo específico.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param file_path Ruta completa al archivo a leer
        @return Contenido del archivo como texto
        @throws FileNotFoundError Si el archivo no existe
        @throws PermissionError Si no hay permisos para leer el archivo
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"El archivo {file_path} no existe")
            
            # Verificar que es un archivo (no un directorio)
            if not os.path.isfile(file_path):
                return f"Error: {file_path} no es un archivo válido"
            
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Limitar el contenido si es muy largo
            max_length = 10000
            if len(content) > max_length:
                content = content[:max_length] + f"\n\n... (contenido truncado, archivo muy largo: {len(content)} caracteres)"
            
            return f"Contenido del archivo {file_path}:\n\n{content}"
            
        except UnicodeDecodeError:
            return f"Error: No se puede leer {file_path} como archivo de texto (posiblemente es un archivo binario)"
        except PermissionError:
            return f"Error: No hay permisos para leer el archivo {file_path}"
        except Exception as e:
            return f"Error al leer el archivo {file_path}: {str(e)}"


class ProjectFileFinderTool(BaseTool):
    """
    Herramienta para encontrar archivos específicos en el proyecto.
    
    Esta herramienta ayuda al agente a localizar archivos importantes
    como package.json, angular.json, etc.
    """
    
    name: str = "file_finder"
    description: str = "Encuentra archivos específicos en el proyecto (ej: package.json, angular.json, etc.)"
    args_schema: type[BaseModel] = ProjectStructureInput
    
    def _run(self, project_path: str) -> str:
        """
        Busca archivos importantes en el proyecto.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param project_path Ruta al directorio del proyecto
        @return Lista de archivos importantes encontrados
        @throws FileNotFoundError Si el directorio del proyecto no existe
        """
        try:
            if not os.path.exists(project_path):
                raise FileNotFoundError(f"El directorio {project_path} no existe")
            
            # Archivos importantes a buscar
            important_files = [
                'package.json', 'angular.json', 'tsconfig.json', 'README.md',
                'requirements.txt', 'setup.py', 'pyproject.toml', 'Cargo.toml',
                'pom.xml', 'build.gradle', 'Gemfile', 'composer.json',
                'Dockerfile', 'docker-compose.yml', '.gitignore'
            ]
            
            found_files = []
            project_root = Path(project_path)
            
            for file_name in important_files:
                file_path = project_root / file_name
                if file_path.exists():
                    found_files.append(str(file_path))
            
            if found_files:
                return f"Archivos importantes encontrados:\n" + "\n".join(f"- {file}" for file in found_files)
            else:
                return "No se encontraron archivos importantes conocidos en el proyecto."
                
        except Exception as e:
            return f"Error al buscar archivos: {str(e)}" 