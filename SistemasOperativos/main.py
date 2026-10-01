import logging
import os
import time
import multiprocessing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import psutil

from orchestration.simulation_manager import SimulationManager
from monitoring.system_monitor import build_process_tree

# --- Configuración de Logs ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S"
)

app = FastAPI(title="Sistema de Monitoreo Analítico")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

manager = SimulationManager()
base_processes = []
stress_processes = []

# --- Tareas Permanentes del Servidor ---
def grandchild_task():
    logging.info(f"proceso Auxiliar_Monitoreo creado - PID {os.getpid()}")
    while True: time.sleep(2)

def base_task(name):
    logging.info(f"proceso {name} creado - PID {os.getpid()}")
    if name == "monitoring":
        p_nieto = multiprocessing.Process(target=grandchild_task, name="Auxiliar_Monitoreo")
        # El nieto sí puede ser daemon porque no tendrá hijos
        p_nieto.daemon = True
        p_nieto.start()
    while True: time.sleep(2)

@app.on_event("startup")
def startup_event():
    logging.info(f"main.py iniciado - PID {os.getpid()}")
    nombres_procesos = ["processing", "monitoring", "storage", "reports"]
    for nombre in nombres_procesos:
        p = multiprocessing.Process(target=base_task, args=(nombre,), name=nombre)
        # DEBE ser False para que Python le permita tener hijos (el nieto)
        p.daemon = False 
        p.start()
        base_processes.append(p)

@app.on_event("shutdown")
def shutdown_event():
    logging.info("Apagando servidor, limpiando procesos base...")
    for p in base_processes:
        if p.is_alive():
            p.terminate()

# --- ENDPOINTS API ---
@app.get("/")
def read_index(): return FileResponse("frontend/index.html")

@app.get("/api/state")
def get_full_state():
    return {
        "metrics": {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
        },
        "experiments": manager.get_state(),
        "tree": build_process_tree()
    }

# --- ENDPOINTS INDIVIDUALES ---
@app.post("/api/simulation/cpu")
def simular_cpu():
    logging.info("carga CPU iniciada")
    p = manager.start_cpu()
    stress_processes.append(p)
    return {"message": "CPU Stress started"}

@app.post("/api/simulation/memory")
def simular_memoria():
    logging.info("crecimiento de memoria iniciado")
    p = manager.start_memory()
    stress_processes.append(p)
    return {"message": "Memory Stress started"}

@app.post("/api/simulation/race")
def simular_carrera():
    logging.info("condición de carrera generada")
    manager.run_race_problem()
    logging.info("resultado incorrecto detectado")
    return {"message": "Race problem generated"}

@app.post("/api/simulation/race/fix")
def corregir_carrera():
    logging.info("corrección Race Condition iniciada")
    manager.run_race_fix()
    logging.info("Lock aplicado, condición de carrera corregida")
    return {"message": "Race fix applied"}

@app.post("/api/simulation/deadlock")
def simular_deadlock():
    logging.info("deadlock generado")
    manager.run_deadlock_problem()
    return {"message": "Deadlock generated"}

@app.post("/api/simulation/deadlock/fix")
def solucionar_deadlock():
    logging.info("corrección Deadlock iniciada")
    manager.run_deadlock_fix()
    return {"message": "Deadlock fix applied"}

@app.post("/api/simulation/producer-consumer")
def simular_productor_consumidor():
    logging.info("Productor-Consumidor iniciado")
    manager.run_producer_consumer()
    return {"message": "Producer Consumer executed"}

# --- ENDPOINTS GLOBALES ---
@app.post("/api/simulation/all")
def generar_todos():
    simular_cpu()
    simular_memoria()
    simular_carrera()
    simular_deadlock()
    return {"message": "Todos los problemas generados"}

@app.post("/api/simulation/fix-all")
def corregir_todos():
    logging.info("aplicando solución total (bajando CPU y RAM, fijando locks)")
    manager.stop_cpu()
    manager.stop_memory()
    corregir_carrera()
    solucionar_deadlock()
    simular_productor_consumidor()
    return {"message": "Todos los problemas corregidos y recursos liberados"}

@app.post("/api/simulation/stop-all")
def detener_todos():
    logging.info("deteniendo experimentos a la fuerza")
    manager.stop_cpu()
    manager.stop_memory()
    manager.reset_state()
    return {"message": "Todo detenido"}

@app.get("/api/logs")
def get_logs():
    try:
        with open("logs/system.log", "r") as f:
            return {"logs": f.read()}
    except:
        return {"logs": ""}

if __name__ == "__main__":
    import uvicorn
    multiprocessing.freeze_support() 
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
