# 🤖 Agente de IA para Análisis de Proyectos

Un agente inteligente desarrollado con **LangGraph** y **Python** que puede analizar la estructura de proyectos de desarrollo, leer archivos y proporcionar descripciones detalladas de la organización del código.

## ✨ Características

- **Análisis de estructura**: Genera un árbol de directorios del proyecto
- **Detección de archivos importantes**: Identifica archivos clave como `package.json`, `angular.json`, `README.md`, etc.
- **Lectura de archivos**: Lee y analiza el contenido de archivos específicos
- **Análisis inteligente**: Utiliza IA para proporcionar descripciones detalladas del proyecto
- **Soporte multiplataforma**: Funciona en Windows, Linux y macOS
- **Interfaz de línea de comandos**: Fácil de usar desde la terminal

## 🛠️ Herramientas del Agente

### 1. **ProjectStructureTool**
- Obtiene la estructura de directorios del proyecto
- Utiliza el comando `tree` en sistemas Unix/Linux
- Implementación alternativa para Windows
- Excluye directorios innecesarios (node_modules, .git, etc.)

### 2. **FileReaderTool**
- Lee el contenido de archivos específicos
- Soporte para archivos de texto
- Límite de contenido para archivos muy grandes
- Manejo de errores de codificación

### 3. **ProjectFileFinderTool**
- Busca archivos importantes en el proyecto
- Identifica archivos de configuración comunes
- Soporte para múltiples tipos de proyectos

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **Clave de API de OpenAI**
- **Git** (para clonar el repositorio)

## 🚀 Instalación

### Opción 1: Instalación Automática (Recomendada)

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd langgraph-agent

# Ejecutar el instalador automático
python setup.py
```

El instalador automático:
- ✅ Verifica la versión de Python
- ✅ Crea el entorno virtual
- ✅ Instala todas las dependencias
- ✅ Configura el archivo de variables de entorno
- ✅ Ejecuta pruebas básicas
- ✅ Muestra instrucciones de uso

### Opción 2: Instalación Manual

#### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd langgraph-agent
```

#### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

Copia el archivo de ejemplo y configura tu clave de API:

```bash
# Windows
copy env.example .env

# Linux/macOS
cp env.example .env
```

Edita el archivo `.env` y agrega tu clave de API de OpenAI:

```env
OPENAI_API_KEY=tu_clave_de_api_aqui
```

**Nota**: Obtén tu clave de API en [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

#### 5. Verificar la instalación

```bash
python test_agent.py
```

## 🎯 Uso

### Uso Básico

```bash
python main.py /ruta/al/proyecto
```

### Ejemplos de Uso

```bash
# Analizar un proyecto Angular
python main.py C:\Users\Usuario\Desktop\mi-proyecto-angular

# Analizar un proyecto React
python main.py /home/usuario/proyectos/mi-app-react

# Usar clave de API como parámetro
python main.py --api-key tu_clave_aqui /ruta/al/proyecto

# Guardar resultados en archivo JSON
python main.py --output resultados.json /ruta/al/proyecto
```

### Parámetros Disponibles

- `project_path`: Ruta al directorio del proyecto (requerido)
- `--api-key`: Clave de API de OpenAI (opcional, puede usar variable de entorno)
- `--output`: Archivo de salida para guardar resultados (opcional)

## 📊 Salida del Agente

El agente proporciona un análisis completo que incluye:

1. **Estructura del proyecto**: Árbol de directorios
2. **Archivos importantes**: Lista de archivos clave encontrados
3. **Contenido de archivo muestra**: Lectura de un archivo representativo
4. **Análisis final**: Descripción detallada del proyecto generada por IA

### Ejemplo de Salida

```
================================================================================
📊 ANÁLISIS DEL PROYECTO
================================================================================

📍 Ruta del proyecto: C:\Users\Usuario\Desktop\mi-proyecto-angular

--------------------------------------------------------------------------------
🌳 ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------------------------
└── mi-proyecto-angular
    ├── src
    │   ├── app
    │   │   ├── components
    │   │   ├── services
    │   │   └── app.component.ts
    │   ├── assets
    │   └── index.html
    ├── package.json
    ├── angular.json
    └── README.md

--------------------------------------------------------------------------------
📁 ARCHIVOS IMPORTANTES
--------------------------------------------------------------------------------
- C:\Users\Usuario\Desktop\mi-proyecto-angular\package.json
- C:\Users\Usuario\Desktop\mi-proyecto-angular\angular.json
- C:\Users\Usuario\Desktop\mi-proyecto-angular\README.md

--------------------------------------------------------------------------------
🤖 ANÁLISIS FINAL
--------------------------------------------------------------------------------
Este es un proyecto Angular que sigue la estructura estándar del framework...

✅ Análisis completado
================================================================================
```

## 🏗️ Arquitectura del Proyecto

```
langgraph-agent/
├── src/
│   ├── tools/
│   │   ├── __init__.py
│   │   └── project_analyzer.py      # Herramientas del agente
│   └── agent/
│       ├── __init__.py
│       └── project_analyzer_agent.py # Agente principal con LangGraph
├── main.py                          # Script principal
├── requirements.txt                 # Dependencias
├── .gitignore
├── env.example                      # Variables de entorno de ejemplo
└── README.md
```

## 🔧 Desarrollo

### Estructura del Código

- **`src/tools/`**: Contiene las herramientas que el agente puede usar
- **`src/agent/`**: Contiene la lógica principal del agente con LangGraph
- **`main.py`**: Script principal con interfaz de línea de comandos

### Agregar Nuevas Herramientas

Para agregar una nueva herramienta:

1. Crea una nueva clase que herede de `BaseTool` en `src/tools/project_analyzer.py`
2. Implementa el método `_run()` con la lógica de la herramienta
3. Agrega la herramienta a la lista en `ProjectAnalyzerAgent.__init__()`

### Personalizar el Flujo

El flujo del agente se define en `_build_workflow()` en `ProjectAnalyzerAgent`. Puedes modificar los nodos y bordes para cambiar el comportamiento del agente.

## 🐛 Solución de Problemas

### Error: "No se encontró la variable de entorno OPENAI_API_KEY"

```bash
# Solución: Crear archivo .env con tu clave de API
echo "OPENAI_API_KEY=tu_clave_aqui" > .env
```

### Error: "El directorio no existe"

```bash
# Solución: Verificar que la ruta sea correcta
python main.py "C:\Users\Usuario\Desktop\mi-proyecto"
```

### Error: "No se puede leer como archivo de texto"

El agente no puede leer archivos binarios. Esto es normal para archivos como imágenes, ejecutables, etc.

### Error de dependencias

```bash
# Solución: Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

## 📝 Licencia

Este proyecto está desarrollado por **Fabian Silva** para **Consulti**.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

**Fabian Silva** - [fabian.silva@consulti.ec](mailto:fabian.silva@consulti.ec)

---

**Nota**: Este agente utiliza la API de OpenAI para generar análisis. Asegúrate de tener créditos suficientes en tu cuenta de OpenAI. 

## 📦 Paquetes Utilizados

El agente utiliza los siguientes paquetes principales:

- **langgraph v0.1.5**: Framework para crear flujos de trabajo con IA
- **langchain v0.1.9**: Biblioteca para construir aplicaciones con LLMs
- **langchain-openai v0.0.8**: Integración con la API de OpenAI
- **python-dotenv v1.0.0**: Manejo de variables de entorno
- **pathlib2 v2.3.7**: Manipulación de rutas de archivos

Para instalar todas las dependencias:
