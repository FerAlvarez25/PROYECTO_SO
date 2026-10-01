import threading
import time
import os

# Ruta al archivo físico compartido
DATOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")
ARCHIVO = os.path.join(DATOS_DIR, "resultados.txt")

def incrementar(iterations):
    """Varios hilos leen y modifican el archivo al mismo tiempo sin protección"""
    for _ in range(iterations):
        # 1. LEER
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        valor = int(contenido) if contenido else 0
        
        # 2. SIMULAR PÉRDIDA DE CPU (para garantizar la colisión)
        time.sleep(0.001) 
        
        # 3. MODIFICAR Y ESCRIBIR
        valor += 1
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write(str(valor))

def run_race_condition():
    os.makedirs(DATOS_DIR, exist_ok=True)
    # Inicializar archivo en 0
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write("0")
        
    iterations = 100 # Menos iteraciones porque escribir a disco físico es más lento que en RAM
    threads = []
    
    # Creamos 4 hilos accediendo al mismo archivo simultáneamente
    for _ in range(4): 
        t = threading.Thread(target=incrementar, args=(iterations,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    # Leer el valor final del archivo
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        actual = int(f.read().strip())
        
    expected = iterations * 4
    return expected, actual

if __name__ == "__main__":
    print("Iniciando prueba de Condición de Carrera en Archivo (Sin Lock)...")
    expected, actual = run_race_condition()
    print(f"Esperado: {expected}")
    print(f"Obtenido del archivo: {actual}")
    if expected != actual:
        print("ERROR: Condición de carrera reproducida exitosamente en archivo.")
