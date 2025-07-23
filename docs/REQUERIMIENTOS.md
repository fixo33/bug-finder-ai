# Requerimientos del Proyecto POC: Agente Bug Finder

## 1. Descripción General

Este proyecto es un **POC (Proof of Concept)** para un agente inteligente capaz de analizar código fuente y detectar bugs, errores y problemas de calidad de manera automática. El componente principal es el **Bug Finder Agent**, un agente especializado que utiliza modelos de lenguaje y herramientas de análisis para identificar y reportar problemas en archivos de código.

---

## 2. Requerimientos Funcionales

### 2.1. Análisis de Código

- [HECHO] El agente debe ser capaz de analizar archivos de código fuente en diferentes lenguajes (Python, JavaScript, Java, C/C++, SQL, etc.).
- [HECHO] Debe detectar:
  - Errores de sintaxis (paréntesis no balanceados, variables no declaradas, etc.).
  - Errores de lógica (condiciones incorrectas, bucles infinitos, etc.).
  - Problemas de seguridad (inyección SQL, XSS, exposición de datos sensibles, etc.).
  - Problemas de rendimiento (bucles ineficientes, consultas N+1, etc.).
  - Problemas de mantenibilidad (código duplicado, funciones largas, falta de documentación, etc.).
  - Errores específicos por lenguaje (por ejemplo, indentación en Python, NullPointerException en Java, memory leaks en C/C++).

- [PENDIENTE] Se requiere que dada una ruta de un proyecto analice los archivos de todo el proyecto en busca de bugs.
- [PENDIENTE] Para evitar que la IA lea en una sola sesión todos los archivos y no sobrepase la ventana de contexto, dividir el análisis en trozos, puede ser por archivo o por cantidad de palabras.
- [PENDIENTE] En el caso de que se quede a la mitad del análisis, el sistema debe crear un archivo donde guarde el estado de los archivos analizados y los que faltan por analizar, para poder continuar si se le pasa la misma ruta del proyecto.
- [PENDIENTE] Por cada bug encontrado o en cada revisión, ir actualizando un archivo con los bugs encontrados con detalles del proyecto, archivo, y otros campos que se usan en el reporte.
- [PENDIENTE] Para los archivos de reporte y estado, analizar cuál conviene para esta primera POC: pueden ser .md o mejor .csv u otro formato. Por el momento manejarlo así; luego se puede optar por algo más robusto como una API o integrar BD.
- [PENDIENTE] Estos archivos servirán de contexto para que la IA pueda realizar mejores análisis.

---

## 2.4. Estrategia de Persistencia de Análisis

Para este POC se utilizarán **tres tipos de archivos**, cada uno con un propósito específico:

### a) `.csv` — Registro tabular de bugs y progreso
- **Uso:** Almacenar y actualizar de forma incremental los bugs encontrados y el estado de los archivos analizados.
- **Ventajas:** Fácil de procesar automáticamente (Python, Excel, pandas, etc.), ideal para listas de bugs, campos fijos y seguimiento de progreso.
- **Ejemplo de campos:**  
  `proyecto,archivo,linea,tipo,severidad,descripcion,sugerencia,fecha`
- **Ejemplo de uso:**  
  Cada vez que se detecta un bug o se analiza un archivo, se agrega o actualiza una fila en el archivo `.csv`.

### b) `.md` — Reportes legibles y documentación
- **Uso:** Generar reportes finales, resúmenes ejecutivos o documentación para usuarios.
- **Ventajas:** Muy legible y presentable, permite incluir tablas, secciones, explicaciones y recomendaciones.
- **Ejemplo de uso:**  
  Al finalizar el análisis de un proyecto, se genera un reporte en Markdown con el resumen y detalles de los bugs encontrados.

### c) `.json` — Estado y contexto complejo del análisis
- **Uso:** Guardar el estado del análisis (archivos ya revisados, pendientes, progreso, contexto adicional) de forma estructurada.
- **Ventajas:** Permite guardar estructuras complejas (listas, diccionarios, progreso por archivo, errores por archivo, etc.), fácil de leer y escribir desde Python.
- **Ejemplo de estructura:**
  ```json
  {
    "proyecto": "mi_proyecto",
    "analizados": ["a.py", "b.py"],
    "pendientes": ["c.py"],
    "bugs": [
      {"archivo": "a.py", "linea": 10, "tipo": "lógica", "descripcion": "...", "severidad": "ALTA"}
    ]
  }
  ```
- **Ejemplo de uso:**  
  Si el análisis se interrumpe, al reanudar se lee el archivo `.json` para continuar desde donde se quedó.

---

### 2.5. Resumen de la estrategia

- **.csv:** Para listas tabulares de bugs y progreso.
- **.md:** Para reportes legibles y documentación.
- **.json:** Para guardar el estado y contexto del análisis de manera estructurada.

Esto permite flexibilidad, facilidad de uso y migración futura a sistemas más robustos (API, base de datos, etc.), sin complicar la implementación inicial.

---

### 2.2. Formato de Respuesta

- [HECHO] El agente debe entregar un reporte estructurado con:
  - Tipo de bug
  - Línea donde se encuentra
  - Descripción detallada
  - Severidad (ALTA, MEDIA, BAJA)
  - Sugerencia de solución
- [HECHO] Debe incluir un resumen con el total de bugs encontrados y recomendaciones generales.

### 2.3. Interfaz de Uso

- [HECHO] El agente debe exponer métodos para analizar un archivo individual o múltiples archivos.
- [HECHO] Debe validar la existencia del archivo antes de analizarlo y manejar errores de forma robusta.

---

## 3. Requerimientos Técnicos

### 3.1. Dependencias

- [HECHO] Python 3.8 o superior
- [HECHO] Paquetes principales:
  - `langchain`
  - `langgraph`
  - `openai` y/o `google_genai` (según el proveedor de modelo)
  - Otras dependencias listadas en `requirements.txt`

### 3.2. Estructura del Código

- [HECHO] El agente principal se encuentra en `src/agent/bug_finder_agent.py`.
- [HECHO] Utiliza un modelo de lenguaje configurable (por defecto: `gemini-2.0-flash` de Google).
- [HECHO] Implementa prompts personalizados para el análisis de bugs.
- [HECHO] Usa herramientas auxiliares como `CodeReaderTool` para la lectura de archivos.

### 3.3. Configuración

- [HECHO] El modelo, proveedor y temperatura son configurables al instanciar el agente.
- [HECHO] Se debe proveer una clave API válida para el proveedor de modelo seleccionado (ver `.env.example`).

---

## 4. Requerimientos de Documentación

- [HECHO] Todo el código público debe estar documentado usando Javadoc adaptado a Python, siguiendo el formato especificado en las reglas del repositorio.
- [HECHO] La documentación debe incluir:
  - Descripción de clases y métodos
  - Parámetros, valores de retorno y excepciones
  - Autor y versión

---

## 5. Ejemplo de Uso

```python
from src.agent.bug_finder_agent import BugFinderAgent

agent = BugFinderAgent(model_name="gemini-2.0-flash", model_provider="google_genai")
resultado = agent.analyze_file("ruta/al/archivo.py")
print(resultado["analysis"])
```

---

## 6. Consideraciones Adicionales

- [HECHO] El agente debe ser exhaustivo pero preciso en sus análisis.
- [HECHO] El sistema debe ser fácilmente extensible para soportar nuevos lenguajes o tipos de análisis.
- [HECHO] Se recomienda ejecutar los análisis en entornos controlados para evitar la exposición de información sensible.

---

## 7. Requerimientos Funcionales Pendientes y Sugerencias

- [PENDIENTE] Implementar análisis recursivo de proyectos completos a partir de una ruta.
- [PENDIENTE] Implementar segmentación del análisis para no sobrepasar la ventana de contexto del modelo.
- [PENDIENTE] Persistencia del estado de análisis para reanudar procesos interrumpidos.
- [PENDIENTE] Registro incremental de bugs encontrados en archivos de reporte.
- [PENDIENTE] Definir y documentar el formato de los archivos de estado y reporte (.md, .csv, .json).
- [PENDIENTE] Utilizar los archivos de reporte/estado como contexto para análisis futuros.

### Sugerencias adicionales:
- [ANÁLISIS] Considerar la integración futura con una base de datos o API para gestión de reportes y estados.
- [ANÁLISIS] Evaluar la posibilidad de análisis incremental (solo archivos modificados desde el último análisis).
- [ANÁLISIS] Añadir métricas de cobertura del análisis y tiempos de ejecución.

---

**Autor:** Fabian Silva <fabian.silva@consulti.ec>  
**Versión:** 1.0 

---

## 8. Detalles de Implementación

Para detalles sobre cómo se implementarán estos requerimientos, flujos técnicos, ejemplos de código y decisiones de arquitectura, consulta el documento:

➡️ [docs/IMPLEMENTACION.md](IMPLEMENTACION.md) 