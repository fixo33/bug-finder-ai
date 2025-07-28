# Flujos de Análisis — Agente Bug Finder

Este documento describe los flujos actuales y los nuevos flujos propuestos para el análisis de bugs, utilizando diagramas Mermaid y descripciones en Markdown.

---

## Índice
1. [Flujo actual: Análisis de un archivo](#flujo-actual-análisis-de-un-archivo)
2. [Flujo actual: Análisis de múltiples archivos](#flujo-actual-análisis-de-múltiples-archivos)
3. [Flujo propuesto: Análisis de todo un proyecto](#flujo-propuesto-análisis-de-todo-un-proyecto)
4. [Comparación y consideraciones](#comparación-y-consideraciones)

---

## 1. Flujo actual: Análisis de un archivo

```mermaid
flowchart TD
    A[Inicio] --> B[Usuario indica archivo a analizar]
    B --> C[Se crea instancia de BugFinderAgent]
    C --> D[Se llama a analyze_file(file_path)]
    D --> E{¿Existe el archivo?}
    E -- No --> F[Retornar error: archivo no existe]
    E -- Sí --> G[Se lee el archivo con CodeReaderTool]
    G --> H[Se crea mensaje de usuario con prompt]
    H --> I[Se ejecuta el agente con el mensaje]
    I --> J[Se extrae contenido del análisis]
    J --> K[Se genera resultado con éxito]
    K --> L[Se muestra el resultado al usuario]
    L --> M[Fin]
    F --> M
```

**Detalles del flujo:**
- El agente utiliza `CodeReaderTool` para leer el contenido del archivo
- Se aplica un prompt específico para análisis de bugs
- El resultado incluye el análisis completo y metadatos del archivo

---

## 2. Flujo actual: Análisis de múltiples archivos

```mermaid
flowchart TD
    A[Inicio] --> B[Usuario indica lista de archivos]
    B --> C[Se crea instancia de BugFinderAgent]
    C --> D[Se llama a analyze_multiple_files(file_paths)]
    D --> E[Para cada archivo en la lista:]
    E --> F[Se llama a analyze_file(file_path)]
    F --> G{¿Existe el archivo?}
    G -- No --> H[Agregar error a resultados]
    G -- Sí --> I[Se lee el archivo con CodeReaderTool]
    I --> J[Se ejecuta el agente con el mensaje]
    J --> K[Se extrae contenido del análisis]
    K --> L[Agregar resultado exitoso a lista]
    H --> M{¿Hay más archivos?}
    L --> M
    M -- Sí --> E
    M -- No --> N[Se muestra el resumen al usuario]
    N --> O[Fin]
```

**Detalles del flujo:**
- Itera sobre cada archivo de la lista proporcionada
- Cada archivo se analiza individualmente usando el mismo flujo que `analyze_file`
- Los resultados se acumulan en una lista que se retorna al final

---

## 3. Flujo propuesto: Análisis de todo un proyecto

```mermaid
flowchart TD
    A[Inicio] --> B[Usuario indica ruta de proyecto]
    B --> C[Se llama a analyze_project(project_path)]
    C --> D[Se configuran rutas de archivos de estado]
    D --> E[Se lee archivo de estado .json existente]
    E --> F[Se listan todos los archivos de código válidos<br/>find_code_files() con exclusiones]
    F --> G[Se inicializan listas: analizados, pendientes, bugs]
    G --> H[Para cada archivo pendiente:]
    H --> I{¿Archivo es muy grande?}
    I -- Sí --> J[Se segmenta el archivo<br/>segment_file()]
    I -- No --> K[Se procesa archivo completo]
    J --> L[Para cada segmento:]
    L --> M[Se lee el segmento con CodeReaderTool]
    M --> N[Se ejecuta el agente con prompt + segmento]
    N --> O[Se extrae análisis del resultado]
    O --> P[Se parsean bugs usando regex]
    P --> Q[Se registra cada bug en .csv]
    Q --> R{¿Hay más segmentos?}
    R -- Sí --> L
    R -- No --> S[Se marca archivo como analizado]
    K --> M
    S --> T[Se actualiza estado en .json]
    T --> U{¿Se interrumpe el análisis?}
    U -- Sí --> V[Guardar estado y salir]
    U -- No --> W{¿Hay más archivos?}
    W -- Sí --> H
    W -- No --> X[Se genera reporte final .md]
    X --> Y[Se muestra resumen al usuario]
    Y --> Z[Fin]
    V --> Z
```

**Detalles del flujo:**
- **Exclusiones automáticas**: Se omiten carpetas como `venv/`, `node_modules/`, `.git/`, `__pycache__/`, etc.
- **Persistencia de estado**: Se guarda progreso en archivo `.json` para permitir reanudación
- **Segmentación**: Archivos grandes se dividen en bloques de 200 líneas por defecto
- **Registro incremental**: Los bugs se guardan en archivo `.csv` a medida que se encuentran
- **Reporte final**: Se genera un archivo `.md` con resumen y detalles de todos los bugs

---

## 4. Comparación y consideraciones

### Flujos actuales vs propuesto:

| Aspecto | Flujos actuales | Flujo propuesto |
|---------|----------------|-----------------|
| **Alcance** | Archivos individuales o listas | Proyecto completo |
| **Persistencia** | No | Sí (archivo .json) |
| **Reanudación** | No | Sí |
| **Archivos grandes** | Limitado por contexto | Segmentación automática |
| **Reportes** | Solo en consola | Archivos .csv y .md |
| **Exclusiones** | Manual | Automática por patrones |

### Ventajas del flujo propuesto:
- **Escalabilidad**: Puede manejar proyectos de cualquier tamaño
- **Robustez**: Persiste el estado y permite reanudación
- **Eficiencia**: Omite archivos irrelevantes automáticamente
- **Trazabilidad**: Genera reportes estructurados y persistentes
- **Flexibilidad**: Configurable mediante parámetros

### Consideraciones técnicas:
- El sistema detecta automáticamente el tipo de proyecto y aplica exclusiones apropiadas
- Los archivos de estado permiten reanudar análisis interrumpidos
- La segmentación evita problemas de límites de contexto del modelo
- Los reportes en formato estándar facilitan la integración con otras herramientas

---

**Autor:** Fabian Silva <fabian.silva@consulti.ec>
**Versión:** 1.1 