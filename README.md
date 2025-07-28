# 🐛 Agente BugFinder - Detección Inteligente de Bugs con IA

Un agente especializado desarrollado con **LangGraph** y **Python** que utiliza **Inteligencia Artificial** para detectar automáticamente bugs, errores y problemas de calidad en código de programación.

## ✨ Características Principales

- **🔍 Detección automática de bugs**: Analiza código usando IA para encontrar errores de sintaxis, lógica y seguridad
- **📁 Análisis flexible**: Soporta archivos individuales, listas de archivos o proyectos completos
- **🔄 Persistencia de estado**: Permite reanudar análisis interrumpidos de proyectos grandes
- **📊 Reportes estructurados**: Genera reportes en CSV y Markdown con detalles de bugs encontrados
- **⚡ Segmentación inteligente**: Divide archivos grandes automáticamente para análisis eficiente
- **🚫 Exclusiones automáticas**: Omite carpetas irrelevantes (venv, node_modules, .git, etc.)
- **🎯 Múltiples lenguajes**: Soporta Python, JavaScript, TypeScript, Java, C++, C, SQL

## 🚀 Casos de Uso

### 1. **Análisis de un archivo individual**
```bash
python agent.py
# Analiza el archivo test_buggy_code.py por defecto
```

### 2. **Análisis de múltiples archivos**
```python
from src.agent import BugFinderAgent

bug_finder = BugFinderAgent()
files = ["archivo1.py", "archivo2.js", "archivo3.java"]
results = bug_finder.analyze_multiple_files(files)
```

### 3. **Análisis completo de proyecto**
```python
from src.agent import BugFinderAgent

bug_finder = BugFinderAgent()
result = bug_finder.analyze_project("/ruta/al/proyecto")
```

## 📋 Flujos de Análisis

El agente BugFinder implementa tres flujos principales de análisis, cada uno optimizado para diferentes escenarios:

### 🔍 **Flujo 1: Análisis de Archivo Individual**
- **Uso**: Para analizar un archivo específico en busca de bugs
- **Ventajas**: Rápido, preciso, ideal para archivos pequeños
- **Proceso**: Lectura → Análisis IA → Reporte inmediato

### 📚 **Flujo 2: Análisis de Múltiples Archivos**
- **Uso**: Para analizar una lista predefinida de archivos
- **Ventajas**: Control total sobre qué archivos analizar
- **Proceso**: Iteración → Análisis individual → Resumen consolidado

### 🏗️ **Flujo 3: Análisis Completo de Proyecto**
- **Uso**: Para analizar automáticamente todo un proyecto
- **Ventajas**: Escalable, persistente, con reanudación automática
- **Proceso**: Exploración → Segmentación → Análisis incremental → Reportes

> 📖 **Documentación detallada**: Consulta [docs/FLUJOS_ANALISIS.md](docs/FLUJOS_ANALISIS.md) para diagramas y explicaciones completas de cada flujo.

## 🛠️ Instalación

### Opción 1: Instalación Automática (Recomendada)

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd langgraph-agent

# Ejecutar el instalador automático
python setup.py
```

### Opción 2: Instalación Manual

```bash
# 1. Clonar y configurar entorno
git clone <url-del-repositorio>
cd langgraph-agent
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key
cp env.example .env
# Editar .env y agregar tu GOOGLE_API_KEY
```

## 🎯 Uso Rápido

### Análisis Básico de Archivo
```bash
# Analizar archivo por defecto
python agent.py

# Analizar archivo específico
python -c "
from src.agent import BugFinderAgent
bug_finder = BugFinderAgent()
result = bug_finder.analyze_file('mi_archivo.py')
print(result['analysis'])
"
```

### Análisis de Proyecto Completo
```python
from src.agent import BugFinderAgent

# Crear agente
bug_finder = BugFinderAgent(
    model_name="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.1
)

# Analizar proyecto completo
result = bug_finder.analyze_project(
    project_path="./mi-proyecto",
    max_lines_per_segment=200,
    exclude_dirs={".git", "node_modules", "venv"}
)

print(f"Bugs encontrados: {result['total_bugs']}")
print(f"Reporte guardado en: {result['md_path']}")
```

## 📊 Tipos de Bugs Detectados

### 🔴 **Errores de Sintaxis**
- Paréntesis, llaves o corchetes no balanceados
- Puntos y coma faltantes
- Palabras clave mal escritas
- Variables no declaradas

### 🟡 **Errores de Lógica**
- Condiciones siempre verdaderas o falsas
- Bucles infinitos potenciales
- División por cero
- Acceso a índices fuera de rango
- Variables no inicializadas

### 🟠 **Problemas de Seguridad**
- Inyección SQL
- Cross-site scripting (XSS)
- Validación de entrada insuficiente
- Exposición de información sensible

### 🔵 **Problemas de Rendimiento**
- Bucles ineficientes
- Consultas N+1
- Memoria no liberada
- Recursos no cerrados

### 🟢 **Problemas de Mantenibilidad**
- Código duplicado
- Funciones muy largas
- Nombres de variables poco descriptivos
- Falta de documentación

## 📈 Reportes y Salidas

### Archivos Generados

1. **`bug_finder_bugs.csv`**: Lista detallada de todos los bugs encontrados
2. **`bug_finder_report.md`**: Reporte completo con resumen y detalles
3. **`bug_finder_state.json`**: Estado del análisis para reanudación

### Ejemplo de Reporte CSV
```csv
proyecto,archivo,linea,tipo,severidad,descripcion,sugerencia,fecha
mi-proyecto,src/main.py,15,Variable no inicializada,ALTA,La variable 'x' se usa antes de ser inicializada,Inicializar 'x' antes de usarla,2024-01-15
mi-proyecto,src/utils.py,42,División por cero,MEDIA,Posible división por cero en línea 42,Agregar validación para evitar división por cero,2024-01-15
```

### Ejemplo de Reporte Markdown
```markdown
# Reporte de Bugs — Proyecto: mi-proyecto

## Resumen
- Total de bugs: 5
- Alta severidad: 2
- Media severidad: 2
- Baja severidad: 1

## Detalle de Bugs
| Archivo | Línea | Tipo | Severidad | Descripción | Sugerencia |
|---------|-------|------|-----------|-------------|------------|
| src/main.py | 15 | Variable no inicializada | ALTA | La variable 'x' se usa antes de ser inicializada | Inicializar 'x' antes de usarla |
```

## ⚙️ Configuración Avanzada

### Parámetros del Agente
```python
bug_finder = BugFinderAgent(
    model_name="gemini-2.0-flash",    # Modelo de IA a usar
    model_provider="google_genai",     # Proveedor (google_genai, openai)
    temperature=0.1                    # Creatividad del modelo (0.0-1.0)
)
```

### Parámetros de Análisis de Proyecto
```python
result = bug_finder.analyze_project(
    project_path="./proyecto",           # Ruta del proyecto
    state_path="./estado.json",          # Archivo de estado personalizado
    csv_path="./bugs.csv",               # Archivo CSV personalizado
    md_path="./reporte.md",              # Archivo MD personalizado
    max_lines_per_segment=200,           # Líneas por segmento
    exclude_dirs={".git", "node_modules"}, # Carpetas a excluir
    exclude_patterns=["*.log", "*.tmp"]   # Patrones a excluir
)
```

## 🔧 Desarrollo y Extensión

### Estructura del Proyecto
```
langgraph-agent/
├── src/
│   ├── agent/
│   │   ├── bug_finder_agent.py        # Agente principal de detección de bugs
│   │   └── project_analyzer_agent.py  # Agente de análisis de proyectos
│   └── tools/
│       ├── code_reader.py             # Herramienta de lectura de código
│       ├── project_analysis_utils.py  # Utilidades de análisis
│       └── project_analyzer.py        # Herramientas de análisis
├── docs/
│   └── FLUJOS_ANALISIS.md             # Documentación de flujos
├── agent.py                           # Script principal para análisis de archivos
├── main.py                            # Script para análisis de proyectos
└── requirements.txt                   # Dependencias
```

### Agregar Nuevos Tipos de Bugs
Para agregar detección de nuevos tipos de bugs, modifica el prompt del sistema en `BugFinderAgent._get_system_prompt()`.

### Personalizar Exclusiones
```python
# Exclusiones personalizadas
exclude_dirs = {".git", "node_modules", "venv", "build", "dist"}
exclude_patterns = ["*.log", "*.tmp", "*.cache", "*.pyc"]
```

## 🐛 Solución de Problemas

### Error: "No se encontró GOOGLE_API_KEY"
```bash
# Solución: Configurar API key en .env
echo "GOOGLE_API_KEY=tu_clave_aqui" > .env
```

### Error: "Archivo no existe"
```bash
# Verificar que la ruta sea correcta
python agent.py  # Usa archivo por defecto
```

### Análisis muy lento en proyectos grandes
```python
# Usar segmentación más pequeña
result = bug_finder.analyze_project(
    project_path="./proyecto",
    max_lines_per_segment=100  # Reducir de 200 a 100
)
```

### Reanudar análisis interrumpido
```python
# El análisis se reanuda automáticamente desde el último estado
result = bug_finder.analyze_project("./proyecto")
# Si se interrumpe, ejecutar el mismo comando para reanudar
```

## 📚 Documentación Adicional

- **[Flujos de Análisis](docs/FLUJOS_ANALISIS.md)**: Diagramas y explicaciones detalladas de los flujos
- **[README Bug Finder](README_BUG_FINDER.md)**: Documentación específica del agente de bugs
- **[Ejemplos](example_*.py)**: Scripts de ejemplo para diferentes casos de uso

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

## 📞 Contacto

**Fabian Silva** - [fabian.silva@consulti.ec](mailto:fabian.silva@consulti.ec)

---

**Nota**: Este agente utiliza la API de Google Gemini para generar análisis. Asegúrate de tener créditos suficientes en tu cuenta de Google AI Studio.

## 📦 Dependencias Principales

- **langgraph v0.1.5**: Framework para flujos de trabajo con IA
- **langchain v0.1.9**: Biblioteca para aplicaciones con LLMs
- **google-generativeai**: Integración con Google Gemini
- **python-dotenv v1.0.0**: Manejo de variables de entorno
- **pathlib2 v2.3.7**: Manipulación de rutas de archivos 
