import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

# Corrección: Forzar un orden jerárquico estricto en la adquisición
def hilo_1():
    print("Hilo 1 adquiriendo Lock A...")
    with lock_a:
        time.sleep(0.1)
        print("Hilo 1 esperando Lock B...")
        with lock_b:
            print("Hilo 1 terminó su trabajo.")

def hilo_2():
    print("Hilo 2 adquiriendo Lock A (Corregido: Antes pedía B)...")
    with lock_a:
        time.sleep(0.1)
        print("Hilo 2 esperando Lock B...")
        with lock_b:
            print("Hilo 2 terminó su trabajo.")

def run_deadlock_fixed():
    t1 = threading.Thread(target=hilo_1)
    t2 = threading.Thread(target=hilo_2)
    
    t1.start()
    t2.start()
    
    t1.join(timeout=3)
    t2.join(timeout=3)
    
    if t1.is_alive() or t2.is_alive():
        return "DEADLOCK DETECTADO"
    return "COMPLETADO SIN PROBLEMAS"

if __name__ == "__main__":
    print("Iniciando simulación de Deadlock Corregida...")
    resultado = run_deadlock_fixed()
    print(f"Estado final: {resultado}")
