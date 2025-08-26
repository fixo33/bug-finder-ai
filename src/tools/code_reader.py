"""
Herramienta para leer archivos de código de programación.

Este módulo contiene una herramienta especializada para leer y analizar
archivos de código de diferentes lenguajes de programación.
"""

import os
from pathlib import Path
from typing import Dict, List, Set
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class CodeFileInput(BaseModel):
    """Modelo de entrada para la herramienta de lectura de código."""
    
    file_path: str = Field(
        description="Ruta completa al archivo de código que se desea leer y analizar"
    )


class CodeReaderTool(BaseTool):
    """
    Herramienta especializada para leer archivos de código de programación.
    
    Esta herramienta puede leer archivos de múltiples lenguajes de programación
    y proporciona información contextual sobre el tipo de archivo y su contenido.
    """
    
    name: str = "code_reader"
    description: str = "Lee y analiza archivos de código de programación de cualquier extensión (.py, .js, .ts, .java, .html, .css, etc.)"
    args_schema: type[BaseModel] = CodeFileInput
    
    # Extensiones de archivos de programación soportadas
    SUPPORTED_EXTENSIONS: Set[str] = {
        # Python
        '.py', '.pyx', '.pyi', '.pyw',
        # JavaScript/TypeScript
        '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
        # Java
        '.java', '.class', '.jar',
        # C/C++
        '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx',
        # C#
        '.cs', '.csproj',
        # PHP
        '.php', '.phtml',
        # Ruby
        '.rb', '.erb',
        # Go
        '.go',
        # Rust
        '.rs',
        # Swift
        '.swift',
        # Kotlin
        '.kt', '.kts',
        # Scala
        '.scala',
        # HTML/CSS
        '.html', '.htm', '.xhtml', '.css', '.scss', '.sass', '.less',
        # XML/JSON
        '.xml', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        # SQL
        '.sql', '.plsql', '.tsql',
        # Shell/Bash
        '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
        # Docker
        '.dockerfile', '.dockerignore',
        # Configuración
        '.env', '.env.local', '.env.production',
        # Markdown
        '.md', '.markdown',
        # Otros
        '.r', '.m', '.pl', '.pm', '.lua', '.dart', '.elm', '.clj', '.edn'
    }
    
    def _run(self, file_path: str) -> str:
        """
        Lee y analiza un archivo de código de programación.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param file_path Ruta completa al archivo de código
        @return Contenido del archivo con información contextual
        @throws FileNotFoundError Si el archivo no existe
        @throws PermissionError Si no hay permisos para leer el archivo
        @throws UnicodeDecodeError Si el archivo no se puede decodificar como texto
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"El archivo {file_path} no existe")
            
            # Obtener información del archivo
            file_path_obj = Path(file_path)
            file_extension = file_path_obj.suffix.lower()
            file_name = file_path_obj.name
            file_size = os.path.getsize(file_path)
            
            # Verificar si es un archivo de código soportado
            is_code_file = file_extension in self.SUPPORTED_EXTENSIONS
            
            # Leer el contenido del archivo
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                # Intentar con encoding alternativo
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    return f"Error: No se pudo leer el archivo {file_path} como texto. Posiblemente es un archivo binario."
            
            # Crear el contexto con información del archivo
            context = self._create_file_context(
                file_name=file_name,
                file_extension=file_extension,
                file_size=file_size,
                is_code_file=is_code_file,
                content=content
            )
            
            return context
            
        except FileNotFoundError as e:
            return f"Error: {str(e)}"
        except PermissionError as e:
            return f"Error: No hay permisos para leer el archivo {file_path}"
        except Exception as e:
            return f"Error inesperado al leer el archivo {file_path}: {str(e)}"
    
    def _create_file_context(self, file_name: str, file_extension: str, 
                           file_size: int, is_code_file: bool, content: str) -> str:
        """
        Crea un contexto informativo sobre el archivo leído.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param file_name Nombre del archivo
        @param file_extension Extensión del archivo
        @param file_size Tamaño del archivo en bytes
        @param is_code_file Si es un archivo de código soportado
        @param content Contenido del archivo
        @return Contexto formateado con información del archivo
        """
        # Determinar el lenguaje de programación
        language = self._get_language_name(file_extension)
        
        # Crear el contexto
        context = f"""=== INFORMACIÓN DEL ARCHIVO ===
Nombre: {file_name}
Extensión: {file_extension}
Lenguaje: {language}
Tamaño: {file_size} bytes
Es archivo de código: {'Sí' if is_code_file else 'No'}

=== CONTENIDO DEL ARCHIVO ===
{content}

=== FIN DEL ARCHIVO ===
"""
        return context
    
    def _get_language_name(self, extension: str) -> str:
        """
        Obtiene el nombre del lenguaje de programación basado en la extensión.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param extension Extensión del archivo
        @return Nombre del lenguaje de programación
        """
        language_map = {
            # Python
            '.py': 'Python', '.pyx': 'Python (Cython)', '.pyi': 'Python (Stubs)', '.pyw': 'Python (Windows)',
            # JavaScript/TypeScript
            '.js': 'JavaScript', '.jsx': 'JavaScript (React)', '.ts': 'TypeScript', '.tsx': 'TypeScript (React)',
            '.mjs': 'JavaScript (ES Modules)', '.cjs': 'JavaScript (CommonJS)',
            # Java
            '.java': 'Java', '.class': 'Java (Bytecode)', '.jar': 'Java (Archive)',
            # C/C++
            '.c': 'C', '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++', '.h': 'C/C++ Header', '.hpp': 'C++ Header',
            # C#
            '.cs': 'C#', '.csproj': 'C# Project',
            # PHP
            '.php': 'PHP', '.phtml': 'PHP (HTML)',
            # Ruby
            '.rb': 'Ruby', '.erb': 'Ruby (ERB)',
            # Go
            '.go': 'Go',
            # Rust
            '.rs': 'Rust',
            # Swift
            '.swift': 'Swift',
            # Kotlin
            '.kt': 'Kotlin', '.kts': 'Kotlin Script',
            # Scala
            '.scala': 'Scala',
            # HTML/CSS
            '.html': 'HTML', '.htm': 'HTML', '.xhtml': 'XHTML', '.css': 'CSS', '.scss': 'SCSS', '.sass': 'Sass', '.less': 'Less',
            # XML/JSON
            '.xml': 'XML', '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML', '.toml': 'TOML', '.ini': 'INI', '.cfg': 'Config',
            # SQL
            '.sql': 'SQL', '.plsql': 'PL/SQL', '.tsql': 'T-SQL',
            # Shell/Bash
            '.sh': 'Shell Script', '.bash': 'Bash', '.zsh': 'Zsh', '.fish': 'Fish', '.ps1': 'PowerShell', '.bat': 'Batch', '.cmd': 'Command',
            # Docker
            '.dockerfile': 'Dockerfile', '.dockerignore': 'Docker Ignore',
            # Configuración
            '.env': 'Environment Variables', '.env.local': 'Environment Variables (Local)', '.env.production': 'Environment Variables (Production)',
            # Markdown
            '.md': 'Markdown', '.markdown': 'Markdown',
            # Otros
            '.r': 'R', '.m': 'MATLAB', '.pl': 'Perl', '.pm': 'Perl Module', '.lua': 'Lua', '.dart': 'Dart', '.elm': 'Elm', '.clj': 'Clojure', '.edn': 'Clojure (EDN)'
        }
        
        return language_map.get(extension, f'Archivo con extensión {extension}') 