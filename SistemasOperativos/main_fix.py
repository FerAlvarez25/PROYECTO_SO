from orchestration.simulation_manager import SimulationManager
import sys

def main():
    print("="*60)
    print("          === CORRECCIÓN DEL SISTEMA ===")
    print("="*60)
    
    manager = SimulationManager()
    
    # Detener CPU
    print("[RUN] Deteniendo CPU Worker...")
    manager.stop_cpu()
    print("[OK] CPU Worker detenido.")
    
    # Detener Memoria
    print("[RUN] Deteniendo Memory Worker...")
    manager.stop_memory()
    print("[OK] Memory Worker detenido y referencias liberadas.")
    
    # Corregir Race Condition
    print("[RUN] Sincronizando Race Condition...")
    manager.run_race_fix()
    print("[OK] Race Condition sincronizada (Mutex aplicado).")
    
    # Corregir Deadlock
    print("[RUN] Resolviendo Deadlock...")
    manager.run_deadlock_fix()
    print("[OK] Deadlock corregido (Orden de Locks estricto).")
    
    # Sincronizar Cola
    print("[RUN] Sincronizando Productor-Consumidor...")
    manager.run_producer_consumer()
    print("[OK] Recurso compartido sincronizado (Queue).")
    
    print("\n" + "="*60)
    print("          Sistema estabilizado al 100%.")
    print("="*60)

if __name__ == "__main__":
    main()
