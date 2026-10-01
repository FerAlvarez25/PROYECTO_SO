# Guía de Sustentación del Proyecto de Sistemas Operativos

Esta guía conecta la rúbrica de evaluación con el funcionamiento de tu código para que puedas defenderlo perfectamente.

## 1. Diseño de la solución (10%)
**Lo que debes decir:** 
"Decidimos implementar una arquitectura Cliente-Servidor. El **Backend (Python)** actúa como el proceso principal administrador del sistema operativo. Elegimos Python porque nos permite gestionar procesos pesados con `multiprocessing` (evitando el bloqueo por el GIL de Python) y manejar concurrencia ligera con `threading`. El **Frontend** es un panel de observación que interactúa por API REST, garantizando que el monitoreo no afecte la carga del servidor."

## 2. Implementación (20%)
**Lo que debes mostrar:**
Ejecuta el servidor y abre el Frontend. Muestra cómo al presionar los botones, el sistema responde en tiempo real. Menciona que se cumplen todos los requisitos: hay proceso padre, procesos hijos (se ven en la tabla), hilos, y simulaciones.

## 3. Concurrencia y Sincronización (Condición de Carrera) (20%)
**Lo que debes demostrar:**
- **Identificación/Reproducción:** Presiona "Generar Condición de Carrera". Muestra en el log o en la pantalla que el resultado final **no es el esperado** (ej. se esperaban 4 millones, pero dio menos). 
- **Explicación:** "Esto ocurre porque 4 hilos están leyendo y modificando la misma variable `counter` al mismo tiempo en RAM. Como la operación `v += 1` no es atómica, los hilos se sobreescriben entre sí."
- **Corrección:** Presiona "Corregir Condición Carrera". Muestra que el resultado ahora es exacto. "Lo solucionamos implementando un mecanismo de exclusión mutua (`threading.Lock()`). Ahora, el hilo que adquiere el lock entra a una *sección crítica*, modificando el recurso de forma segura."

## 4. Interbloqueos / Deadlocks (15%)
**Lo que debes demostrar:**
- **Análisis:** "Para que exista un interbloqueo se requieren 4 condiciones (Exclusión mutua, Retener y esperar, No expropiación, Espera circular)."
- **Reproducción:** Presiona "Generar Deadlock". Muestra cómo el Hilo 1 toma el Recurso A, el Hilo 2 toma el Recurso B, y ambos se quedan esperando infinitamente (usamos un timeout en el código para que no se caiga el servidor, pero el log muestra el Deadlock).
- **Corrección:** Presiona "Corregir Deadlock". Muestra cómo ahora funciona rápido. "Lo prevenimos rompiendo la condición de *espera circular*. Impusimos un orden estricto: ahora todos los hilos deben adquirir siempre el Lock A primero, y luego el Lock B. Así es imposible que se crucen."

## 5. Procesos, hilos y recursos (10%)
**Lo que debes demostrar en la terminal de Linux:**
Abre una terminal de Linux paralela al proyecto y ejecuta:
- `ps -ef | grep main.py` para ver el proceso principal (PPID) y los hijos.
- `pstree -p <PID_DEL_MAIN>` para mostrar gráficamente el árbol de procesos que el backend generó.

## 6. CPU y memoria (10%)
**Lo que debes demostrar en la terminal de Linux:**
- Abre `htop` o `top`.
- **CPU:** Presiona "Simular Carga CPU". Muestra cómo en `htop` uno de los núcleos de tu procesador salta al 100%. "Usamos un bucle matemático intensivo en un proceso separado (`multiprocessing.Process`) para estresar la CPU sin bloquear la interfaz."
- **Memoria:** Presiona "Simular Carga Memoria". Muestra en `htop` cómo la columna de `MEM%` del proceso hijo empieza a subir gradualmente. "Logramos esto reservando arreglos masivos de memoria RAM progresivamente, simulando una fuga de memoria (memory leak)."

## 7. Evidencias y Productor-Consumidor (10%)
- Muestra el archivo `logs/system.log`. Ahí queda todo registrado con fechas exactas, lo que prueba que las pruebas son reales y reproducibles.
- Presiona "Simular Productor-Consumidor" y muestra cómo, usando una cola (`queue.Queue`), un hilo produce datos y otro los consume de forma segura y sincronizada.

## 8. Sustentación (5%)
Apóyense en este documento para hablar con seguridad. Toda decisión (usar FastAPI, separar frontend/backend, usar Locks, usar colas para el Productor) está justificada por la necesidad de aislar, controlar y visualizar el comportamiento interno del Sistema Operativo.
