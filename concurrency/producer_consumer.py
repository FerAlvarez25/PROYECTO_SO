import queue
import threading
import time
import os
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "producer_consumer.log")

def log(msg):
    full_msg = f"{time.strftime('%H:%M:%S')} - {msg}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception: pass

def simulate_cryptographic_work(duration, data_string):
    """Mantiene la CPU al 100% simulando trabajo criptográfico pesado (Hashes SHA-256 iterativos)"""
    end_time = time.time() + duration
    current_hash = hashlib.sha256(data_string.encode()).hexdigest()
    while time.time() < end_time:
        current_hash = hashlib.sha256(current_hash.encode()).hexdigest()
    return current_hash

def run_producer_consumer():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== INICIANDO PRODUCTOR-CONSUMIDOR (PID: {os.getpid()}) ===\n")
    buffer = queue.Queue(maxsize=5)

    def producer():
        for i in range(1, 26):
            item = f"Dato-{i}"
            buffer.put(item)
            msg = f"[PRODUCTOR] Generó {item}. (PID: {os.getpid()}, Hilo: {threading.get_native_id()})"
            log(msg)
            simulate_cryptographic_work(2.0, item)

    def consumer():
        for _ in range(25):
            item = buffer.get()
            msg = f"[CONSUMIDOR] Procesó {item}. (PID: {os.getpid()}, Hilo: {threading.get_native_id()})"
            log(msg)
            buffer.task_done()
            simulate_cryptographic_work(2.0, item)

    log(f"--- HILOS CREADOS ---")
    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    
    t_prod.start()
    t_cons.start()
    
    t_prod.join()
    t_cons.join()
    log("--- PRODUCTOR-CONSUMIDOR FINALIZADO ---")

if __name__ == "__main__":
    run_producer_consumer()
    run_producer_consumer()
