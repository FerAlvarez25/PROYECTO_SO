import json
import os
import time
import multiprocessing
from processes.cpu import cpu_stress_task
from processes.memory import memory_stress_task
from concurrency.race import run_race_condition
from concurrency.race_fixed import run_race_condition_fixed
from concurrency.deadlock import run_deadlock
from concurrency.deadlock_fixed import run_deadlock_fixed
from concurrency.producer_consumer import run_producer_consumer

DATOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")
STATE_FILE = os.path.join(DATOS_DIR, "estado_sistema.json")

class SimulationManager:
    def __init__(self):
        os.makedirs(DATOS_DIR, exist_ok=True)
        self.active_processes = {}
        if not os.path.exists(STATE_FILE):
            self.reset_state()

    def get_state(self):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return self.reset_state()

    def update_state(self, key, data):
        state = self.get_state()
        state[key].update(data)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)
        return state

    def reset_state(self):
        initial_state = {
            "cpu": {
                "estado": "INACTIVO",
                "Problema": "Proceso realizando trabajo matemático intensivo.",
                "Antes": "-",
                "Correccion": "Terminación controlada del CPU Worker.",
                "Despues": "-",
                "Mecanismo": "Control de SO (SIGTERM)",
                "pid": None
            },
            "memory": {
                "estado": "INACTIVO",
                "Problema": "Worker incrementando memoria progresivamente.",
                "Antes": "-",
                "Correccion": "Detención del Memory Worker y liberación de referencias.",
                "Despues": "-",
                "Mecanismo": "Gestión de memoria / SIGTERM",
                "pid": None
            },
            "race": {
                "estado": "INACTIVO",
                "Problema": "Varios hilos modifican un recurso compartido simultáneamente.",
                "Antes": "-",
                "Correccion": "Implementación de Mutex para garantizar exclusión mutua.",
                "Despues": "-",
                "Mecanismo": "threading.Lock()"
            },
            "deadlock": {
                "estado": "INACTIVO",
                "Problema": "Espera circular estricta entre hilos intentando tomar recursos.",
                "Antes": "-",
                "Correccion": "Imponer un orden jerárquico global de adquisición.",
                "Despues": "-",
                "Mecanismo": "Orden consistente de Locks"
            },
            "producer_consumer": {
                "estado": "INACTIVO",
                "Problema": "Productores y consumidores compiten por la misma cola insegura.",
                "Antes": "-",
                "Correccion": "Uso de una estructura con variables de condición integradas.",
                "Despues": "-",
                "Mecanismo": "queue.Queue (Sincronización segura)"
            }
        }
        with open(STATE_FILE, "w") as f:
            json.dump(initial_state, f, indent=4)
        return initial_state

    # --- CONTROLES DE EXPERIMENTOS ---
    def start_cpu(self):
        p = multiprocessing.Process(target=cpu_stress_task, args=(600,)) 
        p.start()
        self.update_state("cpu", {"estado": "ACTIVO", "Antes": f"Consumo elevado (PID: {p.pid})", "Despues": "-", "pid": p.pid})
        return p

    def stop_cpu(self):
        state = self.get_state()
        pid = state.get("cpu", {}).get("pid")
        if pid:
            import signal
            try: os.kill(pid, signal.SIGTERM)
            except Exception: pass
        self.update_state("cpu", {"estado": "CONTROLADO", "Despues": "Worker detenido limpiamente. Consumo en bajada.", "pid": None})

    def start_memory(self):
        p = multiprocessing.Process(target=memory_stress_task, args=(600,))
        p.start()
        self.update_state("memory", {"estado": "ACTIVO", "Antes": f"Fuga de RAM iniciada (PID: {p.pid})", "Despues": "-", "pid": p.pid})
        return p

    def stop_memory(self):
        state = self.get_state()
        pid = state.get("memory", {}).get("pid")
        if pid:
            import signal
            try: os.kill(pid, signal.SIGTERM)
            except Exception: pass
        self.update_state("memory", {"estado": "CONTROLADO", "Despues": "Worker detenido. RAM liberada (Garbage Collection).", "pid": None})

    def run_race_problem(self):
        self.update_state("race", {"estado": "EJECUTANDO...", "Antes": "Evaluando...", "Despues": "-"})
        expected, actual = run_race_condition()
        self.update_state("race", {"estado": "PROBLEMA DETECTADO", "Antes": f"Esperado: {expected}\nObtenido: {actual}"})

    def run_race_fix(self):
        self.update_state("race", {"estado": "EJECUTANDO CORRECCIÓN...", "Despues": "Evaluando..."})
        expected, actual = run_race_condition_fixed()
        self.update_state("race", {"estado": "CORREGIDO", "Despues": f"Esperado: {expected}\nObtenido: {actual}"})

    def run_deadlock_problem(self):
        self.update_state("deadlock", {"estado": "EJECUTANDO...", "Antes": "Hilos intentando adquirir Locks...", "Despues": "-"})
        res = run_deadlock()
        self.update_state("deadlock", {"estado": "PROBLEMA DETECTADO", "Antes": f"Resultado: {res}"})

    def run_deadlock_fix(self):
        self.update_state("deadlock", {"estado": "EJECUTANDO CORRECCIÓN...", "Despues": "Adquiriendo en orden estricto..."})
        res = run_deadlock_fixed()
        self.update_state("deadlock", {"estado": "CORREGIDO", "Despues": f"Resultado: {res}"})
        
    def run_producer_consumer(self):
        self.update_state("producer_consumer", {"estado": "EJECUTANDO...", "Antes": "Llenando cola...", "Despues": "-"})
        logs = run_producer_consumer()
        self.update_state("producer_consumer", {"estado": "CORREGIDO", "Despues": f"Finalizado sin errores: {len(logs)} operaciones seguras."})
