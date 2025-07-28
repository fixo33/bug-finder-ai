# IMPLEMENTACIÓN TÉCNICA — Agente Bug Finder

Este documento detalla el **cómo** se implementarán los requerimientos definidos en `REQUERIMIENTOS.md`.

---

## Índice
1. [Estrategia general de análisis](#estrategia-general-de-análisis)
2. [Persistencia de resultados y estado](#persistencia-de-resultados-y-estado)
3. [Flujo de trabajo del análisis](#flujo-de-trabajo-del-análisis)
4. [Estructura de los archivos de persistencia](#estructura-de-los-archivos-de-persistencia)
5. [Consideraciones técnicas y futuras mejoras](#consideraciones-técnicas-y-futuras-mejoras)

---

## 1. Estrategia general de análisis
- Recorrido recursivo de carpetas a partir de una ruta de proyecto.
- **Omisión automática de carpetas y archivos irrelevantes** (dependencias, entornos virtuales, cachés, binarios, control de versiones, etc.) según la tecnología detectada (Python, Node.js, Java, etc.).
- Segmentación del análisis para no sobrepasar la ventana de contexto del modelo (por archivo o por bloques de líneas/palabras).
- Manejo de interrupciones y reanudación del análisis.

### Ejemplo de exclusión:
- Python: `venv/`, `.venv/`, `__pycache__/`, `*.pyc`, `build/`, `dist/`
- Node.js: `node_modules/`, `dist/`, `build/`, `*.log`
- Java: `target/`, `*.class`, `.gradle/`
- General: `.git/`, `.DS_Store`, `logs/`, `tmp/`, archivos binarios

La lista de exclusión es configurable y puede ampliarse en el futuro (por parámetro o archivo `.bugfinderignore`).

## 2. Persistencia de resultados y estado
- Uso de archivos `.csv` para el registro incremental de bugs y progreso.
- Uso de archivos `.md` para reportes legibles y documentación final.
- Uso de archivos `.json` para guardar el estado del análisis (archivos analizados, pendientes, contexto, etc.).

## 3. Flujo de trabajo del análisis
1. El usuario indica la ruta del proyecto a analizar.
2. El sistema recorre recursivamente los archivos válidos.
3. Por cada archivo/trozo:
   - Se analiza y se registran los bugs encontrados en el `.csv`.
   - Se actualiza el estado en el `.json`.
4. Si el análisis se interrumpe, al reanudar se lee el `.json` para continuar.
5. Al finalizar, se genera un reporte `.md` con el resumen y detalles.

## 4. Estructura de los archivos de persistencia
### a) Ejemplo de archivo `.csv`
```
proyecto,archivo,linea,tipo,severidad,descripcion,sugerencia,fecha
mi_proyecto,main.py,10,Error de lógica,ALTA,"Variable no inicializada","Inicializar antes de usar",2024-06-01
```

### b) Ejemplo de archivo `.md`
```
# Reporte de Bugs — Proyecto: mi_proyecto

## Resumen
- Total de bugs: 5
- Alta severidad: 2
- Media severidad: 2
- Baja severidad: 1

## Detalle de Bugs
| Archivo   | Línea | Tipo           | Severidad | Descripción                | Sugerencia                |
|-----------|-------|----------------|-----------|----------------------------|---------------------------|
| main.py   | 10    | Error de lógica| ALTA      | Variable no inicializada   | Inicializar antes de usar |
```

### c) Ejemplo de archivo `.json`
```
{
  "proyecto": "mi_proyecto",
  "analizados": ["main.py"],
  "pendientes": ["utils.py"],
  "bugs": [
    {"archivo": "main.py", "linea": 10, "tipo": "lógica", "descripcion": "Variable no inicializada", "severidad": "ALTA"}
  ]
}
```

## 5. Consideraciones técnicas y futuras mejoras
- Posible integración futura con base de datos o API.
- Análisis incremental (solo archivos modificados).
- Métricas de cobertura y tiempos de ejecución.
- Validaciones y manejo de errores robusto.

---

**Autor:** Fabian Silva <fabian.silva@consulti.ec>
**Versión:** 1.0 