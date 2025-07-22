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
            
            return {
                "success": True,
                "file_path": file_path,
                "analysis": result["messages"][-1]["content"],
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