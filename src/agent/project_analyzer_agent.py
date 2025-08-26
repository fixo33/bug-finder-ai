"""
Agente de IA para análisis de proyectos usando LangGraph.

Este módulo implementa un agente inteligente que puede analizar la estructura
de proyectos de desarrollo, leer archivos y proporcionar descripciones detalladas.
"""

import os
from typing import Dict, List, Any, TypedDict, Annotated
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from dotenv import load_dotenv

from src.tools.project_analyzer import (
    ProjectStructureTool,
    FileReaderTool,
    ProjectFileFinderTool
)

# Cargar variables de entorno
load_dotenv()


class AgentState(TypedDict):
    """
    Estado del agente durante la ejecución.
    
    Define la estructura de datos que mantiene el estado
    del agente durante el análisis del proyecto.
    """
    
    messages: Annotated[List, "Lista de mensajes de la conversación"]
    project_path: Annotated[str, "Ruta al proyecto a analizar"]
    project_structure: Annotated[str, "Estructura del proyecto obtenida"]
    important_files: Annotated[str, "Archivos importantes encontrados"]
    file_content: Annotated[str, "Contenido del archivo leído"]
    analysis: Annotated[str, "Análisis final del proyecto"]


class ProjectAnalyzerAgent:
    """
    Agente de IA para análisis de proyectos de desarrollo.
    
    Este agente utiliza LangGraph para coordinar múltiples herramientas
    y proporcionar un análisis completo de la estructura y contenido
    de proyectos de desarrollo.
    """
    
    def __init__(self, openai_api_key: str = None):
        """
        Inicializa el agente de análisis de proyectos.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param openai_api_key Clave de API de OpenAI (opcional, puede usar variable de entorno)
        @throws ValueError Si no se proporciona la clave de API de OpenAI
        """
        # Configurar la clave de API
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Se requiere OPENAI_API_KEY como parámetro o variable de entorno")
        
        # Inicializar el modelo de lenguaje
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1
        )
        
        # Inicializar herramientas
        self.tools = [
            ProjectStructureTool(),
            FileReaderTool(),
            ProjectFileFinderTool()
        ]
        
        # Crear el nodo de herramientas
        self.tool_node = ToolNode(self.tools)
        
        # Construir el grafo del agente
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Construye el flujo de trabajo del agente usando LangGraph.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @return Grafo de estado que define el flujo del agente
        """
        # Crear el grafo de estado
        workflow = StateGraph(AgentState)
        
        # Agregar nodos
        workflow.add_node("analyze_structure", self._analyze_project_structure)
        workflow.add_node("find_important_files", self._find_important_files)
        workflow.add_node("read_sample_file", self._read_sample_file)
        workflow.add_node("generate_analysis", self._generate_project_analysis)
        workflow.add_node("tools", self.tool_node)
        
        # Definir el flujo
        workflow.set_entry_point("analyze_structure")
        workflow.add_edge("analyze_structure", "find_important_files")
        workflow.add_edge("find_important_files", "read_sample_file")
        workflow.add_edge("read_sample_file", "generate_analysis")
        workflow.add_edge("generate_analysis", END)
        
        # Agregar bordes condicionales para herramientas
        workflow.add_conditional_edges(
            "tools",
            self._should_continue_to_tools,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _analyze_project_structure(self, state: AgentState) -> AgentState:
        """
        Analiza la estructura del proyecto usando la herramienta correspondiente.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param state Estado actual del agente
        @return Estado actualizado con la estructura del proyecto
        """
        try:
            # Usar la herramienta para obtener la estructura
            structure_tool = ProjectStructureTool()
            project_structure = structure_tool._run(state["project_path"])
            
            # Actualizar el estado
            state["project_structure"] = project_structure
            
            # Agregar mensaje informativo
            state["messages"].append(
                AIMessage(content=f"Estructura del proyecto analizada:\n{project_structure}")
            )
            
        except Exception as e:
            state["project_structure"] = f"Error al analizar estructura: {str(e)}"
            state["messages"].append(
                AIMessage(content=f"Error al analizar la estructura del proyecto: {str(e)}")
            )
        
        return state
    
    def _find_important_files(self, state: AgentState) -> AgentState:
        """
        Busca archivos importantes en el proyecto.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param state Estado actual del agente
        @return Estado actualizado con los archivos importantes
        """
        try:
            # Usar la herramienta para encontrar archivos importantes
            file_finder_tool = ProjectFileFinderTool()
            important_files = file_finder_tool._run(state["project_path"])
            
            # Actualizar el estado
            state["important_files"] = important_files
            
            # Agregar mensaje informativo
            state["messages"].append(
                AIMessage(content=f"Archivos importantes encontrados:\n{important_files}")
            )
            
        except Exception as e:
            state["important_files"] = f"Error al buscar archivos: {str(e)}"
            state["messages"].append(
                AIMessage(content=f"Error al buscar archivos importantes: {str(e)}")
            )
        
        return state
    
    def _read_sample_file(self, state: AgentState) -> AgentState:
        """
        Lee un archivo de muestra del proyecto para análisis.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param state Estado actual del agente
        @return Estado actualizado con el contenido del archivo
        """
        try:
            # Buscar un archivo para leer (priorizar README.md, package.json, etc.)
            sample_files = ["README.md", "package.json", "angular.json", "requirements.txt"]
            file_to_read = None
            
            for file_name in sample_files:
                file_path = os.path.join(state["project_path"], file_name)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    file_to_read = file_path
                    break
            
            if file_to_read:
                # Usar la herramienta para leer el archivo
                file_reader_tool = FileReaderTool()
                file_content = file_reader_tool._run(file_to_read)
                
                # Actualizar el estado
                state["file_content"] = file_content
                
                # Agregar mensaje informativo
                state["messages"].append(
                    AIMessage(content=f"Archivo leído: {file_to_read}\n{file_content}")
                )
            else:
                state["file_content"] = "No se encontró ningún archivo de muestra para leer"
                state["messages"].append(
                    AIMessage(content="No se encontró ningún archivo de muestra para leer")
                )
                
        except Exception as e:
            state["file_content"] = f"Error al leer archivo: {str(e)}"
            state["messages"].append(
                AIMessage(content=f"Error al leer archivo de muestra: {str(e)}")
            )
        
        return state
    
    def _generate_project_analysis(self, state: AgentState) -> AgentState:
        """
        Genera un análisis final del proyecto basado en toda la información recopilada.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param state Estado actual del agente
        @return Estado actualizado con el análisis final
        """
        try:
            # Crear prompt para el análisis
            analysis_prompt = f"""
            Basándote en la siguiente información del proyecto, proporciona un análisis detallado:
            
            RUTA DEL PROYECTO: {state['project_path']}
            
            ESTRUCTURA DEL PROYECTO:
            {state['project_structure']}
            
            ARCHIVOS IMPORTANTES:
            {state['important_files']}
            
            CONTENIDO DEL ARCHIVO MUESTRA:
            {state['file_content']}
            
            Por favor, proporciona:
            1. Tipo de proyecto (Angular, React, Python, etc.)
            2. Descripción general de la estructura
            3. Tecnologías utilizadas
            4. Propósito del proyecto (si se puede inferir)
            5. Observaciones importantes sobre la organización del código
            6. Recomendaciones si aplica
            
            Sé específico y detallado en tu análisis.
            """
            
            # Generar análisis usando el modelo
            response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
            analysis = response.content
            
            # Actualizar el estado
            state["analysis"] = analysis
            
            # Agregar mensaje final
            state["messages"].append(
                AIMessage(content=f"Análisis final del proyecto:\n{analysis}")
            )
            
        except Exception as e:
            state["analysis"] = f"Error al generar análisis: {str(e)}"
            state["messages"].append(
                AIMessage(content=f"Error al generar análisis final: {str(e)}")
            )
        
        return state
    
    def _should_continue_to_tools(self, state: AgentState) -> str:
        """
        Determina si el agente debe continuar usando herramientas.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param state Estado actual del agente
        @return "continue" si debe continuar, "end" si debe terminar
        """
        # Por ahora, siempre terminar después de las herramientas
        return "end"
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analiza un proyecto completo y devuelve los resultados.
        
        @author Fabian Silva <devawsoftware@gmail.com>
        @version 1.0
        
        @param project_path Ruta al directorio del proyecto a analizar
        @return Diccionario con todos los resultados del análisis
        @throws FileNotFoundError Si el directorio del proyecto no existe
        @throws Exception Si ocurre un error durante el análisis
        """
        # Verificar que el directorio existe
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"El directorio {project_path} no existe")
        
        if not os.path.isdir(project_path):
            raise ValueError(f"{project_path} no es un directorio válido")
        
        # Inicializar el estado
        initial_state = AgentState(
            messages=[HumanMessage(content=f"Analiza el proyecto en: {project_path}")],
            project_path=project_path,
            project_structure="",
            important_files="",
            file_content="",
            analysis=""
        )
        
        # Ejecutar el flujo de trabajo
        try:
            result = self.workflow.invoke(initial_state)
            return {
                "project_path": project_path,
                "project_structure": result["project_structure"],
                "important_files": result["important_files"],
                "file_content": result["file_content"],
                "analysis": result["analysis"],
                "messages": result["messages"]
            }
        except Exception as e:
            raise Exception(f"Error durante el análisis del proyecto: {str(e)}") 