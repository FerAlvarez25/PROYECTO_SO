import threading
import time
import os

DATOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")
ARCHIVO = os.path.join(DATOS_DIR, "reporte_servidor.txt")

def incrementar(iterations):
    """Varios hilos leen y modifican el archivo al mismo tiempo sin protección"""
    for _ in range(iterations):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        valor = int(contenido) if contenido else 0
        
        time.sleep(0.001) 
        
        valor += 1
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write(str(valor))

def run_race_condition():
    os.makedirs(DATOS_DIR, exist_ok=True)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write("0")
        
    iterations = 100
    threads = []
    
    for _ in range(4): 
        t = threading.Thread(target=incrementar, args=(iterations,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
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
