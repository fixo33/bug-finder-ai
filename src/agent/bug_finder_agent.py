"""
Agente especializado para encontrar bugs de programación.

Este módulo contiene un agente de IA diseñado específicamente para analizar
código fuente y detectar posibles bugs, errores y problemas de calidad.
"""

import os
from typing import List, Dict, Any
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, SystemMessage

from ..tools import CodeReaderTool
from ..tools.project_analysis_utils import (
    find_code_files, read_json_state, write_json_state, append_bug_to_csv, generate_md_report, segment_file
)


class BugFinderAgent:
    """
    Agente especializado para detectar bugs y problemas en código de programación.
    
    Este agente utiliza herramientas especializadas para leer archivos de código
    y analizarlos en busca de errores, bugs y problemas de calidad.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", 
                 model_provider: str = "google_genai", 
                 temperature: float = 0.1):
        """
        Inicializa el agente de detección de bugs.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param model_name Nombre del modelo de IA a utilizar
        @param model_provider Proveedor del modelo (google_genai, openai, etc.)
        @param temperature Temperatura del modelo (0.0 = determinístico, 1.0 = creativo)
        """
        self.model_name = model_name
        self.model_provider = model_provider
        self.temperature = temperature
        
        # Inicializar el modelo
        self.model = init_chat_model(
            model_name, 
            model_provider=model_provider, 
            temperature=temperature
        )
        
        # Configurar las herramientas
        self.tools = [CodeReaderTool()]
        
        # Configurar los prompts
        self.system_prompt = self._get_system_prompt()
        self.user_prompt = self._get_user_prompt()
        
        # Crear el agente
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.system_prompt
        )
    
    def _get_system_prompt(self) -> str:
        """
        Obtiene el prompt del sistema para el agente de detección de bugs.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @return Prompt del sistema configurado
        """
        return """Eres un agente especializado en detección de bugs y análisis de código de programación. Tu misión es analizar archivos de código fuente y encontrar posibles errores, bugs y problemas de calidad.

## TUS CAPACIDADES:
- Puedes leer archivos de código de múltiples lenguajes de programación
- Analizas la sintaxis, lógica y estructura del código
- Detectas errores comunes de programación
- Identificas problemas de seguridad, rendimiento y mantenibilidad
- Proporcionas sugerencias de mejora

## TIPOS DE BUGS QUE DEBES DETECTAR:

### 1. Errores de Sintaxis:
- Paréntesis, llaves o corchetes no balanceados
- Puntos y coma faltantes
- Palabras clave mal escritas
- Variables no declaradas

### 2. Errores de Lógica:
- Condiciones siempre verdaderas o falsas
- Bucles infinitos potenciales
- División por cero
- Acceso a índices fuera de rango
- Variables no inicializadas

### 3. Problemas de Seguridad:
- Inyección SQL
- Cross-site scripting (XSS)
- Exposición de información sensible
- Validación de entrada insuficiente
- Uso de funciones deprecadas o inseguras

### 4. Problemas de Rendimiento:
- Bucles ineficientes
- Consultas N+1
- Memoria no liberada
- Algoritmos de complejidad O(n²) o peor
- Carga de archivos sin límites

### 5. Problemas de Mantenibilidad:
- Código duplicado
- Funciones muy largas
- Variables con nombres poco descriptivos
- Falta de documentación
- Acoplamiento excesivo

### 6. Errores Específicos por Lenguaje:
- **Python**: Indentación incorrecta, imports faltantes, excepciones no manejadas
- **JavaScript/TypeScript**: Undefined/null checks, scope issues, async/await mal usado
- **Java**: NullPointerException, ClassCastException, recursos no cerrados
- **C/C++**: Memory leaks, buffer overflows, punteros no inicializados
- **SQL**: Inyección SQL, consultas ineficientes, transacciones no manejadas

## FORMATO DE RESPUESTA:
Para cada problema encontrado, proporciona:
1. **Tipo de Bug**: Categoría del problema
2. **Línea**: Número de línea donde se encuentra
3. **Descripción**: Explicación detallada del problema
4. **Severidad**: ALTA, MEDIA o BAJA
5. **Sugerencia**: Cómo solucionarlo

## EJEMPLO DE RESPUESTA:
```
=== ANÁLISIS DE BUGS ENCONTRADOS ===

🐛 BUG #1
Tipo: Error de Lógica
Línea: 15
Descripción: Variable 'result' no inicializada antes de su uso
Severidad: ALTA
Sugerencia: Inicializar 'result' con un valor por defecto antes del bucle

🐛 BUG #2
Tipo: Problema de Seguridad
Línea: 23
Descripción: Consulta SQL vulnerable a inyección
Severidad: ALTA
Sugerencia: Usar consultas preparadas o ORM

=== RESUMEN ===
Total de bugs encontrados: 2
Bugs de alta severidad: 2
Bugs de media severidad: 0
Bugs de baja severidad: 0
```

Recuerda: Tu objetivo es ayudar a mejorar la calidad del código y prevenir errores en producción. Sé exhaustivo pero preciso en tu análisis."""
    
    def _get_user_prompt(self) -> str:
        """
        Obtiene el prompt del usuario para solicitar análisis de código.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @return Prompt del usuario configurado
        """
        return """Por favor, analiza el siguiente archivo de código en busca de bugs, errores y problemas de calidad. 

Utiliza la herramienta code_reader para leer el archivo y luego realiza un análisis exhaustivo.

Archivo a analizar: {file_path}

Proporciona un análisis detallado incluyendo:
1. Todos los bugs encontrados con su tipo, línea, descripción, severidad y sugerencia
2. Un resumen con el total de problemas encontrados
3. Recomendaciones generales para mejorar la calidad del código

Sé específico y detallado en tu análisis."""
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analiza un archivo de código en busca de bugs.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param file_path Ruta al archivo de código a analizar
        @return Resultado del análisis con bugs encontrados
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                return {
                    "error": f"El archivo {file_path} no existe",
                    "success": False
                }
            
            # Crear el mensaje del usuario
            user_message = self.user_prompt.format(file_path=file_path)
            
            # Ejecutar el agente
            result = self.agent.invoke({
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            })
            
            # Extraer el contenido del último mensaje
            if "messages" in result and result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    analysis_content = last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    analysis_content = last_message["content"]
                else:
                    analysis_content = str(last_message)
            else:
                analysis_content = str(result)
            
            return {
                "success": True,
                "file_path": file_path,
                "analysis": analysis_content,
                "raw_result": result
            }
            
        except Exception as e:
            return {
                "error": f"Error durante el análisis: {str(e)}",
                "success": False,
                "file_path": file_path
            }
    
    def analyze_multiple_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Analiza múltiples archivos de código en busca de bugs.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param file_paths Lista de rutas a archivos de código
        @return Lista de resultados de análisis
        """
        results = []
        
        for file_path in file_paths:
            result = self.analyze_file(file_path)
            results.append(result)
        
        return results 

    def analyze_project(self, project_path: str, 
                       state_path: str = None, 
                       csv_path: str = None, 
                       md_path: str = None, 
                       max_lines_per_segment: int = 200) -> Dict[str, Any]:
        """
        Analiza recursivamente todos los archivos de código de un proyecto, persiste el estado y genera reportes.
        
        Este método recorre todos los archivos de código válidos en la ruta indicada, analiza cada uno (segmentando si es necesario), registra los bugs encontrados en un archivo .csv, guarda el estado del análisis en un archivo .json para permitir reanudación, y genera un reporte final en .md con el resumen y detalle de bugs.
        
        @author Fabian Silva <fabian.silva@consulti.ec>
        @version 1.0
        
        @param project_path Ruta raíz del proyecto a analizar.
        @param state_path Ruta al archivo .json de estado (opcional, por defecto en la raíz del proyecto).
        @param csv_path Ruta al archivo .csv de bugs (opcional, por defecto en la raíz del proyecto).
        @param md_path Ruta al archivo .md de reporte (opcional, por defecto en la raíz del proyecto).
        @param max_lines_per_segment Máximo de líneas por segmento de archivo a analizar (para evitar sobrepasar la ventana de contexto).
        @return Diccionario con resumen del análisis y rutas de los archivos de reporte.
        @throws Exception Si ocurre un error grave durante el análisis.
        """
        import datetime
        import re
        
        if state_path is None:
            state_path = os.path.join(project_path, 'bug_finder_state.json')
        if csv_path is None:
            csv_path = os.path.join(project_path, 'bug_finder_bugs.csv')
        if md_path is None:
            md_path = os.path.join(project_path, 'bug_finder_report.md')
        
        # Leer estado previo o inicializar
        state = read_json_state(state_path)
        proyecto = os.path.basename(os.path.abspath(project_path))
        analizados = set(state.get('analizados', []))
        pendientes = set(state.get('pendientes', []))
        bugs = state.get('bugs', [])
        
        # Listar archivos válidos
        all_files = set(find_code_files(project_path))
        if not pendientes:
            pendientes = all_files - analizados
        else:
            pendientes = set(pendientes)
        
        # Analizar cada archivo pendiente
        for file_path in list(pendientes):
            try:
                # Segmentar si es grande
                segments = segment_file(file_path, max_lines=max_lines_per_segment)
                for idx, segment in enumerate(segments):
                    # Analizar segmento
                    user_message = self.user_prompt.format(file_path=file_path)
                    # Adjuntar el segmento al mensaje
                    prompt = f"{user_message}\n\n---\n\n{segment}"
                    result = self.agent.invoke({
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    })
                    # Extraer análisis
                    if "messages" in result and result["messages"]:
                        last_message = result["messages"][-1]
                        if hasattr(last_message, 'content'):
                            analysis_content = last_message.content
                        elif isinstance(last_message, dict) and "content" in last_message:
                            analysis_content = last_message["content"]
                        else:
                            analysis_content = str(last_message)
                    else:
                        analysis_content = str(result)
                    # Parsear bugs del análisis (usando regex simple por ahora)
                    bug_pattern = re.compile(r"BUG #[0-9]+.*?Tipo: (.*?)\nLínea: (.*?)\nDescripción: (.*?)\nSeveridad: (.*?)\nSugerencia: (.*?)\n", re.DOTALL)
                    for match in bug_pattern.finditer(analysis_content):
                        tipo, linea, descripcion, severidad, sugerencia = match.groups()
                        bug = {
                            "proyecto": proyecto,
                            "archivo": file_path,
                            "linea": linea.strip(),
                            "tipo": tipo.strip(),
                            "severidad": severidad.strip(),
                            "descripcion": descripcion.strip(),
                            "sugerencia": sugerencia.strip(),
                            "fecha": datetime.date.today().isoformat()
                        }
                        append_bug_to_csv(csv_path, bug, header=["proyecto","archivo","linea","tipo","severidad","descripcion","sugerencia","fecha"])
                        bugs.append(bug)
                # Marcar como analizado
                analizados.add(file_path)
                pendientes.remove(file_path)
                # Guardar estado tras cada archivo
                write_json_state(state_path, {
                    "proyecto": proyecto,
                    "analizados": list(analizados),
                    "pendientes": list(pendientes),
                    "bugs": bugs
                })
            except Exception as e:
                # Si falla, dejar pendiente y continuar
                continue
        # Resumen para el reporte
        total = len(bugs)
        alta = sum(1 for b in bugs if b.get('severidad','').upper() == 'ALTA')
        media = sum(1 for b in bugs if b.get('severidad','').upper() == 'MEDIA')
        baja = sum(1 for b in bugs if b.get('severidad','').upper() == 'BAJA')
        summary = {
            "proyecto": proyecto,
            "total": total,
            "alta": alta,
            "media": media,
            "baja": baja
        }
        generate_md_report(md_path, summary, bugs)
        return {
            "success": True,
            "proyecto": proyecto,
            "total_bugs": total,
            "alta": alta,
            "media": media,
            "baja": baja,
            "csv_path": csv_path,
            "md_path": md_path,
            "state_path": state_path
        } 