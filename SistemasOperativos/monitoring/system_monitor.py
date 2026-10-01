import psutil
import os

def build_process_tree():
    """Construye un árbol jerárquico real usando psutil basado en el PID actual"""
    my_pid = os.getpid()
    
    try:
        main_proc = psutil.Process(my_pid)
    except psutil.NoSuchProcess:
        return "Error: No se pudo localizar el proceso principal."

    tree = []
    
    def add_to_tree(proc, level, prefix=""):
        try:
            name = proc.name()
            pid = proc.pid
            status = proc.status()
            threads = proc.num_threads()
            
            line = f"{prefix}{name} [PID {pid}] - {status.upper()} - {threads} hilos"
            tree.append(line)
            
            children = proc.children()
            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                branch = "└── " if is_last else "├── "
                add_to_tree(child, level + 1, prefix + branch)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    add_to_tree(main_proc, 0)
    return "\n".join(tree)
