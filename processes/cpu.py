import time
import os
import signal

running = True

def sigterm_handler(signum, frame):
    global running
    print(f"\n[CPU WORKER] Señal SIGTERM recibida en PID={os.getpid()}. Apagando de forma segura...")
    running = False

def cpu_stress_task(duration=15):
    global running
    print(f"[CPU WORKER] Iniciado. PID={os.getpid()}")
    
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    end_time = time.time() + duration
    while running and time.time() < end_time:
        _ = [x**2 for x in range(5000)]
        
    print("[CPU WORKER] Finalizado limpiamente. Recursos liberados.")

if __name__ == "__main__":
    cpu_stress_task(10)
