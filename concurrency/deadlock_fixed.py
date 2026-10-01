import threading
import time
import os

lock_a = threading.Lock()
lock_b = threading.Lock()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "deadlock.log")

def log(msg):
    full_msg = f"{time.strftime('%H:%M:%S')} - [SOLUCIÓN] - {msg}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception: pass

def hilo_1():
    log(f"[HILO 1 - TID {threading.get_native_id()}] Intentando leer Base de Datos (Lock A)...")
    with lock_a:
        log(f"[HILO 1 - TID {threading.get_native_id()}] Base de Datos TOMADA. Trabajando 25 segundos...")
        time.sleep(25)
        log(f"[HILO 1 - TID {threading.get_native_id()}] Intentando tomar Lock B (Disco)...")
        with lock_b:
            log(f"[HILO 1] Operación completada exitosamente.")

def hilo_2():
    log(f"[HILO 2 - TID {threading.get_native_id()}] Intentando leer Base de Datos (Lock A) <- ¡CORRECCIÓN!...")
    with lock_a:
        log(f"[HILO 2 - TID {threading.get_native_id()}] Base de Datos TOMADA. Trabajando 25 segundos...")
        time.sleep(25)
        log(f"[HILO 2 - TID {threading.get_native_id()}] Intentando tomar Lock B (Disco)...")
        with lock_b:
            log(f"[HILO 2] Operación completada exitosamente.")

def run_deadlock_fixed():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== INICIANDO PRUEBA DE DEADLOCK CORREGIDO (PID: {os.getpid()}) ===\n")
        
    t1 = threading.Thread(target=hilo_1)
    t2 = threading.Thread(target=hilo_2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    log("AMBOS HILOS TERMINARON SIN BLOQUEARSE. ¡CORRECCIÓN EXITOSA!")

if __name__ == "__main__":
    run_deadlock_fixed()
