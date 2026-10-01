import time
from orchestration.simulation_manager import SimulationManager
from monitoring.system_monitor import build_process_tree

def main():
    print("="*50)
    print(" INICIANDO TODOS LOS PROBLEMAS DEL SISTEMA")
    print("="*50)
    
    manager = SimulationManager()
    manager.reset_state()
    
    print("[1] Iniciando Carga de CPU...")
    p_cpu = manager.start_cpu()
    
    print("[2] Iniciando Fuga de Memoria...")
    p_mem = manager.start_memory()
    
    print("[3] Detonando Condición de Carrera...")
    manager.run_race_problem()
    
    print("[4] Detonando Deadlock (Interbloqueo)...")
    manager.run_deadlock_problem()
    
    print("\nTodos los problemas han sido generados en el Sistema Operativo.")
    print("Puedes usar 'htop', 'ps' o 'pstree' en otra terminal para verificarlos.")
    print("\n--- Árbol de Procesos Actual ---")
    print(build_process_tree())
    
    print("\nPresiona Ctrl+C para detener los procesos de carga (CPU/RAM).")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo procesos...")
        p_cpu.terminate()
        p_mem.terminate()
        manager.reset_state()
        print("Experimentos finalizados.")

if __name__ == "__main__":
    main()
