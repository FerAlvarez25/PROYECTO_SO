# DOCUMENTACIÓN TÉCNICA - LABORATORIO DE SISTEMAS OPERATIVOS

## 1. Arquitectura de la solución
El sistema implementa una arquitectura distribuida tipo Cliente-Servidor de 3 capas, diseñada específicamente para aislar el *overhead* de la interfaz gráfica y mantener la pureza de las métricas del sistema operativo:
*   **Core del Sistema Operativo (Backend Python):** Utiliza los módulos nativos `multiprocessing` y `threading` para interactuar directamente con el Kernel de Linux (mediante System Calls), gestionar memoria, aislar procesos y administrar cerrojos (Locks).
*   **Orquestador y API (FastAPI):** Actúa como middleware mediante un bucle de eventos asíncrono (ASGI/epoll), sirviendo de puente para que las señales de control de los experimentos se envíen al SO. Utiliza `psutil` para inspeccionar el sistema de archivos virtual `/proc` y extraer métricas reales.
*   **Capa de Presentación (JS/HTML):** Un cliente "stateless" (sin estado) totalmente desacoplado que consume la API. Esta separación garantiza que el alto consumo de CPU observado en herramientas como `top` o `htop` sea estrictamente producto de las simulaciones y no del renderizado de la interfaz del usuario.

## 2. Procesos e hilos
Se utilizaron ambos paradigmas para demostrar el control sobre los espacios de memoria:
*   **Procesos (`multiprocessing.Process`):** Se crearon procesos con PIDs independientes y espacios de memoria aislados para evadir el *Global Interpreter Lock (GIL)* de Python. Esto permitió estresar físicamente núcleos reales de la CPU e inflar el *Resident Set Size (RSS)* en memoria sin bloquear el servidor. Adicionalmente, se programó un árbol jerárquico demostrable (`main.py` -> `Monitoreo` -> `Auxiliar_Monitoreo`) reconstruible vía PID/PPID y el comando `pstree`.
*   **Hilos (`threading.Thread`):** Se instanciaron múltiples LWPs (*Light-Weight Processes*) bajo un mismo PID principal compartiendo el mismo espacio de direccionamiento virtual. Esto fue vital para forzar las condiciones de carrera y los interbloqueos, requerimientos centrales del laboratorio.

## 3. Recursos compartidos
Se implementaron dos tipos de recursos compartidos para las pruebas de concurrencia:
1.  **Archivo Físico (I/O):** Un archivo de texto real en disco (`datos/resultados.txt`) utilizado para demostrar colisiones de escritura a nivel del sistema de archivos.
2.  **Cola en Memoria RAM:** Una estructura `queue.Queue` compartida por hilos en el espacio de usuario para el problema del Productor-Consumidor.

## 4. Problema de concurrencia
Se indujo deliberadamente una **Condición de Carrera (Race Condition)**. 
*   **Descripción:** Múltiples hilos intentan realizar operaciones de lectura-modificación-escritura sobre el recurso compartido (`resultados.txt`) simultáneamente.
*   **Causa raíz:** Al carecer de atomicidad, si el planificador de procesos (*Scheduler* de Linux) realiza un cambio de contexto (*Context Switch*) a mitad de la operación de un hilo, el siguiente hilo lee datos obsoletos y sobrescribe el progreso del anterior, generando pérdida de datos e inconsistencia en el valor final esperado.

## 5. Mecanismo de sincronización
Para solucionar los conflictos de concurrencia se implementaron:
*   **Mutex (Exclusión Mutua):** Se aplicó el objeto `threading.Lock()` para envolver las operaciones de I/O en una **Sección Crítica**. Esto asegura que solo un hilo a la vez acceda al archivo físico, obligando a los demás a suspenderse hasta que el cerrojo sea liberado.
*   **Variables de Condición Condicionales:** Se mitigó el desbordamiento de búfer en el Productor-Consumidor delegando la sincronización al objeto `queue.Queue`, el cual internamente bloquea al hilo Productor si la cola alcanza su límite, y bloquea al Consumidor si esta se encuentra vacía.

## 6. Análisis del interbloqueo (Deadlock)
Se forzó un *Deadlock* replicando las condiciones de Coffman, específicamente la **Espera Circular**.
*   **Análisis del Problema:** El Hilo 1 adquiere el `Lock A` y, sin soltarlo, solicita el `Lock B`. Simultáneamente, el Hilo 2 adquiere el `Lock B` y solicita el `Lock A`. Como ninguno cede su recurso, el sistema se bloquea indefinidamente.
*   **Solución Aplicada:** Se solucionó mediante la **Prevención del Interbloqueo**. Se implementó un algoritmo de asignación que obliga a todos los hilos del sistema a adquirir los cerrojos en un **orden jerárquico global y estricto** (Siempre el Lock A primero, y luego el Lock B). Esto destruye matemáticamente la posibilidad de que se forme una espera circular.

## 7. Pruebas de CPU y memoria
*   **CPU:** Se ejecutó un proceso intensivo de cálculos matemáticos pesados en un bucle cerrado, forzando a un núcleo del procesador físico a alcanzar el 100% de uso.
*   **Memoria:** Se simuló una fuga de memoria (*Memory Leak*) inyectando bloques continuos de caracteres pesados a una lista en RAM, inflando la memoria residente del proceso gradualmente. Por seguridad, se implementó un *hard-limit* de 200MB para evitar inestabilidad en la Máquina Virtual.
*   **Solución de Recursos:** La liberación de estos recursos no se hizo matando el programa de raíz, sino enviando una señal asíncrona del sistema operativo (`SIGTERM`). Los *workers* interceptan esta señal, detienen sus bucles, activan el recolector de basura (*Garbage Collector*) para vaciar la RAM de forma limpia, y finalizan su ejecución (Técnica de *Graceful Shutdown*).
