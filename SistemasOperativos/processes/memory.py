import time
import os
import signal

running = True

def sigterm_handler(signum, frame):
    global running
    print(f"\n[MEMORY WORKER] Señal SIGTERM recibida en PID={os.getpid()}. Procediendo a liberar RAM...")
    running = False

def memory_stress_task(duration=15):
    global running
    print(f"[MEMORY WORKER] Iniciado. PID={os.getpid()}")
    
    # Capturar la orden de detención para un cierre limpio
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    end_time = time.time() + duration
    dummy_list = []
    try:
        while running and time.time() < end_time:
            # Límite estricto de 20 bloques (~200MB) para evitar Crash del SO
            if len(dummy_list) < 20:
                dummy_list.append(" " * 10_000_000)
                print(f"[MEMORY WORKER] RAM añadida. Total local: ~{len(dummy_list)*10} MB")
            time.sleep(1)
    except MemoryError:
        print("[MEMORY WORKER] Límite absoluto alcanzado.")
    finally:
        print("[MEMORY WORKER] Liberando referencias (Garbage Collection)...")
        del dummy_list
        print("[MEMORY WORKER] RAM liberada exitosamente.")

if __name__ == "__main__":
    memory_stress_task(10)
