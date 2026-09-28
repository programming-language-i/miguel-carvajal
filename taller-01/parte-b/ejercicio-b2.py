### B2. Daemon con `finally`


import threading
import time


def guardar():
    try:
        time.sleep(2)
        print("guardado")
    finally:
        print("archivo cerrado")


threading.Thread(target=guardar, daemon=True).start()
time.sleep(0.5)
print("fin")


"""
* Funcionamiento del hilo daemon:
Un hilo daemon es un hilo "en segundo plano" que Python trata de forma especial:
cuando el hilo principal (o todos los hilos no-daemon) terminan, el programa se 
cierra sin esperar a que los hilos daemon acaben su trabajo — simplemente se 
"matan" de golpe.

* Suposicion:
El hilo daemon tiene tiempo suficiente para ejecutar la función `guardar()`

* Accion real:
El hilo daemon no tiene tiempo suficiente para ejecutar la función `guardar()`

"""