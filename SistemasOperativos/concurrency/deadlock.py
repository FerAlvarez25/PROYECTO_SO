import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def hilo_1():
    print("Hilo 1 adquiriendo Lock A...")
    lock_a.acquire()
    time.sleep(0.1) # Simula procesamiento
    
    print("Hilo 1 esperando Lock B...")
    lock_b.acquire()
    
    print("Hilo 1 terminó su trabajo.")
    lock_b.release()
    lock_a.release()

def hilo_2():
    print("Hilo 2 adquiriendo Lock B...")
    lock_b.acquire()
    time.sleep(0.1)
    
    print("Hilo 2 esperando Lock A...")
    lock_a.acquire()
    
    print("Hilo 2 terminó su trabajo.")
    lock_a.release()
    lock_b.release()

def run_deadlock():
    t1 = threading.Thread(target=hilo_1)
    t2 = threading.Thread(target=hilo_2)
    
    t1.start()
    t2.start()
    
    t1.join(timeout=3)
    t2.join(timeout=3)
    
    if t1.is_alive() or t2.is_alive():
        return "DEADLOCK DETECTADO"
    return "COMPLETADO"

if __name__ == "__main__":
    print("Iniciando simulación de Deadlock...")
    resultado = run_deadlock()
    print(f"Estado final: {resultado}")
