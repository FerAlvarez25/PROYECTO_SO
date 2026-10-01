import queue
import threading
import time

def run_producer_consumer():
    buffer = queue.Queue(maxsize=5)
    logs = []

    def producer():
        for i in range(1, 6):
            item = f"Dato-{i}"
            buffer.put(item) # Bloquea si el buffer está lleno
            msg = f"Productor: generó {item}"
            print(msg)
            logs.append(msg)
            time.sleep(0.1)

    def consumer():
        for _ in range(5):
            item = buffer.get() # Bloquea si el buffer está vacío
            msg = f"Consumidor: procesó {item}"
            print(msg)
            logs.append(msg)
            buffer.task_done()
            time.sleep(0.2)

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    
    t_prod.start()
    t_cons.start()
    t_prod.join()
    t_cons.join()
    
    return logs

if __name__ == "__main__":
    run_producer_consumer()
