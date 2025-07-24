import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

VALID_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.sql'}


def find_code_files(project_path: str, exts: Optional[List[str]] = None) -> List[str]:
    """
    Recorre recursivamente el proyecto y retorna una lista de archivos de código válidos.
    
    @author Fabian Silva <fabian.silva@consulti.ec>
    @version 1.0
    
    @param project_path Ruta raíz del proyecto
    @param exts Lista de extensiones válidas (opcional)
    @return Lista de rutas de archivos de código
    """
    if exts is None:
        exts = list(VALID_EXTENSIONS)
    code_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                code_files.append(os.path.join(root, file))
    return code_files


def read_json_state(state_path: str) -> Dict[str, Any]:
    """
    Lee el archivo de estado .json si existe, o retorna estructura vacía.
    """
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def write_json_state(state_path: str, state: Dict[str, Any]):
    """
    Escribe el estado en un archivo .json.
    """
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def append_bug_to_csv(csv_path: str, bug: Dict[str, Any], header: Optional[List[str]] = None):
    """
    Agrega un bug al archivo .csv, creando el archivo si no existe.
    """
    file_exists = os.path.exists(csv_path)
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header or bug.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(bug)


def generate_md_report(md_path: str, summary: Dict[str, Any], bugs: List[Dict[str, Any]]):
    """
    Genera un reporte .md con resumen y detalle de bugs.
    """
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Reporte de Bugs — Proyecto: {summary.get('proyecto', '')}\n\n")
        f.write("## Resumen\n")
        f.write(f"- Total de bugs: {summary.get('total', 0)}\n")
        f.write(f"- Alta severidad: {summary.get('alta', 0)}\n")
        f.write(f"- Media severidad: {summary.get('media', 0)}\n")
        f.write(f"- Baja severidad: {summary.get('baja', 0)}\n\n")
        f.write("## Detalle de Bugs\n")
        f.write("| Archivo   | Línea | Tipo           | Severidad | Descripción                | Sugerencia                |\n")
        f.write("|-----------|-------|----------------|-----------|----------------------------|---------------------------|\n")
        for bug in bugs:
            f.write(f"| {bug.get('archivo','')} | {bug.get('linea','')} | {bug.get('tipo','')} | {bug.get('severidad','')} | {bug.get('descripcion','')} | {bug.get('sugerencia','')} |\n")


def segment_file(file_path: str, max_lines: int = 200) -> List[str]:
    """
    Divide un archivo grande en bloques de líneas para análisis incremental.
    """
    segments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(0, len(lines), max_lines):
        segment = ''.join(lines[i:i+max_lines])
        segments.append(segment)
    return segments 