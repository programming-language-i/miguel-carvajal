### B1. ¿Cuánto tarda?


import threading
import time


def tarea(n):
    time.sleep(1)


inicio = time.perf_counter()
for i in range(3):
    hilo = threading.Thread(target=tarea, args=(i,))
    hilo.start()
    hilo.join()
print(f"{time.perf_counter() - inicio:.1f} s")


"""
* Tiempo supuesto: 3.0 s
Este codigo tarda 3 segundos en ejecutarse, ya que cada hilo se tiene
un tiempo de espera de 1 segundo y se ejecutan de manera secuencial
debido al uso de join() inmediatamente después de start().

* Tiempo real: 3.0 s

"""

