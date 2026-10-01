import threading
import time
import os

lock_a = threading.Lock()
lock_b = threading.Lock()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "deadlock.log")

def log(msg):
    full_msg = f"{time.strftime('%H:%M:%S')} - {msg}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception: pass

def hilo_1():
    log(f"[HILO 1 - TID {threading.get_native_id()}] Intentando leer Base de Datos (Lock A)...")
    lock_a.acquire()
    log(f"[HILO 1 - TID {threading.get_native_id()}] Base de Datos BLOQUEADA. Procesando 25 segundos...")
    time.sleep(25) 
    
    log(f"[HILO 1 - TID {threading.get_native_id()}] Intentando tomar Lock B (Disco)...")
    lock_b.acquire()
    
    log(f"[HILO 1] Operación completada.")
    lock_b.release()
    lock_a.release()

def hilo_2():
    log(f"[HILO 2 - TID {threading.get_native_id()}] Escribiendo en Disco (Lock B)...")
    lock_b.acquire()
    log(f"[HILO 2 - TID {threading.get_native_id()}] Disco BLOQUEADO. Procesando 25 segundos...")
    time.sleep(25)
    
    log(f"[HILO 2 - TID {threading.get_native_id()}] Intentando tomar Lock A (BD)...")
    lock_a.acquire()
    
    log(f"[HILO 2] Operación completada.")
    lock_a.release()
    lock_b.release()

def run_deadlock():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== INICIANDO SIMULACIÓN DE DEADLOCK (PID: {os.getpid()}) ===\n")
        
    t1 = threading.Thread(target=hilo_1)
    t2 = threading.Thread(target=hilo_2)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

if __name__ == "__main__":
    run_deadlock()
