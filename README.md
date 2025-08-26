# Agente de Detección de Bugs de Programación

Este proyecto implementa un agente de IA especializado en detectar bugs, errores y problemas de calidad en código de programación de múltiples lenguajes.
# Agente de Detección de Bugs de Programación

Este proyecto implementa un agente de IA especializado en detectar bugs, errores y problemas de calidad en código de programación de múltiples lenguajes.

## 🚀 Características

### Herramienta de Lectura de Código (`CodeReaderTool`)
- **Soporte multi-lenguaje**: Lee archivos de más de 50 extensiones diferentes
- **Información contextual**: Proporciona metadatos del archivo (lenguaje, tamaño, etc.)
- **Manejo robusto de errores**: Gestiona archivos binarios, permisos y encoding
- **Lenguajes soportados**:
  - Python (.py, .pyx, .pyi, .pyw)
  - JavaScript/TypeScript (.js, .jsx, .ts, .tsx, .mjs, .cjs)
  - Java (.java, .class, .jar)
  - C/C++ (.c, .cpp, .cc, .cxx, .h, .hpp, .hxx)
  - C# (.cs, .csproj)
  - PHP (.php, .phtml)
  - Ruby (.rb, .erb)
  - Go (.go)
  - Rust (.rs)
  - Swift (.swift)
  - Kotlin (.kt, .kts)
  - Scala (.scala)
  - HTML/CSS (.html, .htm, .xhtml, .css, .scss, .sass, .less)
  - XML/JSON (.xml, .json, .yaml, .yml, .toml, .ini, .cfg)
  - SQL (.sql, .plsql, .tsql)
  - Shell/Bash (.sh, .bash, .zsh, .fish, .ps1, .bat, .cmd)
  - Docker (.dockerfile, .dockerignore)
  - Y muchos más...

### Agente de Detección de Bugs (`BugFinderAgent`)
- **Análisis exhaustivo**: Detecta múltiples tipos de problemas
- **Categorización de bugs**: Clasifica por severidad y tipo
- **Sugerencias de mejora**: Proporciona soluciones específicas
- **Prompts especializados**: Optimizado para análisis de código

## 🐛 Tipos de Bugs Detectados
## 🚀 Características

### Herramienta de Lectura de Código (`CodeReaderTool`)
- **Soporte multi-lenguaje**: Lee archivos de más de 50 extensiones diferentes
- **Información contextual**: Proporciona metadatos del archivo (lenguaje, tamaño, etc.)
- **Manejo robusto de errores**: Gestiona archivos binarios, permisos y encoding
- **Lenguajes soportados**:
  - Python (.py, .pyx, .pyi, .pyw)
  - JavaScript/TypeScript (.js, .jsx, .ts, .tsx, .mjs, .cjs)
  - Java (.java, .class, .jar)
  - C/C++ (.c, .cpp, .cc, .cxx, .h, .hpp, .hxx)
  - C# (.cs, .csproj)
  - PHP (.php, .phtml)
  - Ruby (.rb, .erb)
  - Go (.go)
  - Rust (.rs)
  - Swift (.swift)
  - Kotlin (.kt, .kts)
  - Scala (.scala)
  - HTML/CSS (.html, .htm, .xhtml, .css, .scss, .sass, .less)
  - XML/JSON (.xml, .json, .yaml, .yml, .toml, .ini, .cfg)
  - SQL (.sql, .plsql, .tsql)
  - Shell/Bash (.sh, .bash, .zsh, .fish, .ps1, .bat, .cmd)
  - Docker (.dockerfile, .dockerignore)
  - Y muchos más...

### Agente de Detección de Bugs (`BugFinderAgent`)
- **Análisis exhaustivo**: Detecta múltiples tipos de problemas
- **Categorización de bugs**: Clasifica por severidad y tipo
- **Sugerencias de mejora**: Proporciona soluciones específicas
- **Prompts especializados**: Optimizado para análisis de código

## 🐛 Tipos de Bugs Detectados

### 1. Errores de Sintaxis
### 1. Errores de Sintaxis
- Paréntesis, llaves o corchetes no balanceados
- Puntos y coma faltantes
- Palabras clave mal escritas
- Variables no declaradas

### 2. Errores de Lógica
### 2. Errores de Lógica
- Condiciones siempre verdaderas o falsas
- Bucles infinitos potenciales
- División por cero
- Acceso a índices fuera de rango
- Variables no inicializadas

### 3. Problemas de Seguridad
### 3. Problemas de Seguridad
- Inyección SQL
- Cross-site scripting (XSS)
- Exposición de información sensible
- Exposición de información sensible
- Validación de entrada insuficiente
- Uso de funciones deprecadas o inseguras
- Uso de funciones deprecadas o inseguras

### 4. Problemas de Rendimiento
### 4. Problemas de Rendimiento
- Bucles ineficientes
- Consultas N+1
- Memoria no liberada
- Algoritmos de complejidad O(n²) o peor
- Carga de archivos sin límites
- Algoritmos de complejidad O(n²) o peor
- Carga de archivos sin límites

### 5. Problemas de Mantenibilidad
### 5. Problemas de Mantenibilidad
- Código duplicado
- Funciones muy largas
- Variables con nombres poco descriptivos
- Variables con nombres poco descriptivos
- Falta de documentación
- Acoplamiento excesivo

### 6. Errores Específicos por Lenguaje
- **Python**: Indentación incorrecta, imports faltantes, excepciones no manejadas
- **JavaScript/TypeScript**: Undefined/null checks, scope issues, async/await mal usado
- **Java**: NullPointerException, ClassCastException, recursos no cerrados
- **C/C++**: Memory leaks, buffer overflows, punteros no inicializados
- **SQL**: Inyección SQL, consultas ineficientes, transacciones no manejadas

## 📦 Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd bug-finder-ai
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
```bash
cp env.example .env
# Editar .env con tu API key de Google
```

## 🎯 Uso

### Uso Básico

```python
from src.agent import BugFinderAgent

# Crear el agente
from src.agent import BugFinderAgent

# Crear el agente
bug_finder = BugFinderAgent(
    model_name="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.1
)

# Analizar un archivo
result = bug_finder.analyze_file("mi_archivo.py")

if result["success"]:
    print(result["analysis"])
else:
    print(f"Error: {result['error']}")
```

### Uso con Ruta Estática

El archivo `agent.py` ya está configurado para analizar el archivo `test_buggy_code.py`:

```bash
python agent.py
```

### Probar la Herramienta de Lectura

```bash
python test_code_reader.py
    model_name="gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.1
)

# Analizar un archivo
result = bug_finder.analyze_file("mi_archivo.py")

if result["success"]:
    print(result["analysis"])
else:
    print(f"Error: {result['error']}")
```

### Uso con Ruta Estática

El archivo `agent.py` ya está configurado para analizar el archivo `test_buggy_code.py`:

```bash
python agent.py
```

### Probar la Herramienta de Lectura

```bash
python test_code_reader.py
```

## 📁 Estructura del Proyecto

## 📁 Estructura del Proyecto

```
bug-finder-ai/
├── src/
│   ├── tools/
│   │   ├── code_reader.py          # Herramienta de lectura de código
│   │   ├── project_analyzer.py     # Herramientas de análisis de proyecto
│   │   └── __init__.py
│   └── agent/
│       ├── bug_finder_agent.py     # Agente de detección de bugs
│       ├── project_analyzer_agent.py
│       └── __init__.py
├── agent.py                        # Script principal
├── test_buggy_code.py             # Archivo con bugs intencionales
├── test_code_reader.py            # Script de prueba
└── README_BUG_FINDER.md           # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

```env
GOOGLE_API_KEY=tu_api_key_aqui
```

### Parámetros del Agente

- **model_name**: Nombre del modelo de IA (default: "gemini-2.0-flash")
- **model_provider**: Proveedor del modelo (default: "google_genai")
- **temperature**: Temperatura del modelo (0.0 = determinístico, 1.0 = creativo)

## 📊 Formato de Salida

El agente proporciona un análisis estructurado:

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

## 🧪 Pruebas

### Archivo de Prueba
El archivo `test_buggy_code.py` contiene 17 bugs intencionales de diferentes tipos para probar el agente.

### Scripts de Prueba
- `test_code_reader.py`: Prueba la herramienta de lectura de código
- `agent.py`: Ejecuta el agente completo

## 🤝 Contribución
│   ├── tools/
│   │   ├── code_reader.py          # Herramienta de lectura de código
│   │   ├── project_analyzer.py     # Herramientas de análisis de proyecto
│   │   └── __init__.py
│   └── agent/
│       ├── bug_finder_agent.py     # Agente de detección de bugs
│       ├── project_analyzer_agent.py
│       └── __init__.py
├── agent.py                        # Script principal
├── test_buggy_code.py             # Archivo con bugs intencionales
├── test_code_reader.py            # Script de prueba
└── README_BUG_FINDER.md           # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

```env
GOOGLE_API_KEY=tu_api_key_aqui
```

### Parámetros del Agente

- **model_name**: Nombre del modelo de IA (default: "gemini-2.0-flash")
- **model_provider**: Proveedor del modelo (default: "google_genai")
- **temperature**: Temperatura del modelo (0.0 = determinístico, 1.0 = creativo)

## 📊 Formato de Salida

El agente proporciona un análisis estructurado:

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

## 🧪 Pruebas

### Archivo de Prueba
El archivo `test_buggy_code.py` contiene 17 bugs intencionales de diferentes tipos para probar el agente.

### Scripts de Prueba
- `test_code_reader.py`: Prueba la herramienta de lectura de código
- `agent.py`: Ejecuta el agente completo

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor
## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Fabian Silva** - [devawsoftware@gmail.com](mailto:devawsoftware@gmail.com)

## 🙏 Agradecimientos

- LangGraph por el framework de agentes
- Google Gemini por el modelo de IA
- La comunidad de desarrolladores por las mejores prácticas de detección de bugs 
## 🙏 Agradecimientos

- LangGraph por el framework de agentes
- Google Gemini por el modelo de IA
- La comunidad de desarrolladores por las mejores prácticas de detección de bugs 