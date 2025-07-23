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
    D --> E[Se lee el archivo con CodeReaderTool]
    E --> F[El modelo IA analiza el contenido]
    F --> G[Se genera reporte de bugs]
    G --> H[Se muestra el resultado al usuario]
    H --> I[Fin]
```

---

## 2. Flujo actual: Análisis de múltiples archivos

```mermaid
flowchart TD
    A[Inicio] --> B[Usuario indica lista de archivos]
    B --> C[Se crea instancia de BugFinderAgent]
    C --> D[Se llama a analyze_multiple_files(file_paths)]
    D --> E[Para cada archivo:]
    E --> F[Se lee el archivo con CodeReaderTool]
    F --> G[El modelo IA analiza el contenido]
    G --> H[Se agrega resultado a la lista]
    H --> I[Se muestra el resumen al usuario]
    I --> J[Fin]
```

---

## 3. Flujo propuesto: Análisis de todo un proyecto

```mermaid
flowchart TD
    A[Inicio] --> B[Usuario indica ruta de proyecto]
    B --> C[Se listan todos los archivos de código válidos]
    C --> D[Se crea/lee archivo de estado (.json)]
    D --> E[Para cada archivo pendiente:]
    E --> F[Se lee el archivo con CodeReaderTool]
    F --> G[El modelo IA analiza el contenido]
    G --> H[Se registra bug en .csv]
    H --> I[Se actualiza estado en .json]
    I --> J{¿Se interrumpe el análisis?}
    J -- Sí --> K[Guardar estado y salir]
    J -- No --> L[¿Hay más archivos?]
    L -- Sí --> E
    L -- No --> M[Generar reporte final .md]
    M --> N[Mostrar resumen al usuario]
    N --> O[Fin]
```

---

## 4. Comparación y consideraciones

- El flujo actual permite analizar archivos individuales o listados, pero no persiste el estado ni soporta proyectos grandes.
- El nuevo flujo soporta análisis de proyectos completos, persistencia de estado, reanudación y registro incremental de bugs.
- Se mantiene compatibilidad con el análisis de archivos individuales o listados.

---

**Autor:** Fabian Silva <fabian.silva@consulti.ec>
**Versión:** 1.0 