"""
Archivo de prueba con bugs intencionales para testear el agente de detección de bugs.

Este archivo contiene varios tipos de errores comunes de programación
para verificar que el agente los detecte correctamente.
"""

import os
import sqlite3
from typing import List, Dict

# Bug 1: Variable no inicializada
def calculate_average(numbers):
    total = 0
    count = 0
    
    for num in numbers:
        total += num
        count += 1
    
    # Bug: División por cero potencial
    return total / count  # Si numbers está vacío, count será 0

# Bug 2: Variable no declarada
def process_data(data):
    result = []
    
    for item in data:
        # Bug: Variable 'processed_item' no está definida
        result.append(processed_item)
    
    return result

# Bug 3: Inyección SQL
def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Bug: Consulta SQL vulnerable a inyección
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    return user

# Bug 4: Manejo de excepciones inadecuado
def read_file_content(file_path):
    # Bug: No maneja excepciones
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Bug 5: Recursos no liberados
def create_connection():
    conn = sqlite3.connect('database.db')
    # Bug: Conexión no se cierra
    return conn

# Bug 6: Lógica incorrecta
def is_even(number):
    # Bug: Lógica incorrecta para verificar si es par
    if number % 2 == 1:
        return True
    return False

# Bug 7: Acceso a índice fuera de rango
def get_first_element(items):
    # Bug: No verifica si la lista está vacía
    return items[0]

# Bug 8: Variable global mal usada
global_var = 0

def increment_global():
    global global_var
    global_var += 1
    # Bug: No retorna nada, pero debería

# Bug 9: Función muy larga (más de 20 líneas)
def very_long_function():
    print("Línea 1")
    print("Línea 2")
    print("Línea 3")
    print("Línea 4")
    print("Línea 5")
    print("Línea 6")
    print("Línea 7")
    print("Línea 8")
    print("Línea 9")
    print("Línea 10")
    print("Línea 11")
    print("Línea 12")
    print("Línea 13")
    print("Línea 14")
    print("Línea 15")
    print("Línea 16")
    print("Línea 17")
    print("Línea 18")
    print("Línea 19")
    print("Línea 20")
    print("Línea 21")  # Demasiadas líneas

# Bug 10: Import no utilizado
import json  # Bug: Import no utilizado

# Bug 11: Variable con nombre poco descriptivo
def process(x):
    # Bug: Variable 'x' no es descriptiva
    y = x * 2
    return y

# Bug 12: Comentario obsoleto
# Esta función suma dos números
def multiply(a, b):
    # Bug: Comentario incorrecto, la función multiplica, no suma
    return a * b

# Bug 13: Hardcoded values
def calculate_tax(amount):
    # Bug: Tasa de impuesto hardcodeada
    tax_rate = 0.15
    return amount * tax_rate

# Bug 14: Función sin documentación
def undocumented_function(param1, param2):
    # Bug: Función sin docstring
    return param1 + param2

# Bug 15: Múltiples returns en función simple
def simple_function(x):
    if x > 0:
        return True
    elif x < 0:
        return False
    else:
        return None  # Bug: Múltiples returns innecesarios

if __name__ == "__main__":
    # Bug 16: Código de prueba que puede fallar
    numbers = [1, 2, 3, 4, 5]
    print(calculate_average(numbers))
    
    # Bug 17: Llamada a función que puede fallar
    empty_list = []
    print(get_first_element(empty_list))  # Esto causará IndexError 