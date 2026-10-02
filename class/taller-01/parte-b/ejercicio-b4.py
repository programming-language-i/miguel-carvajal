### B4. Reiniciar un hilo


import threading

hilo = threading.Thread(target=print, args=("hola",))
hilo.start()
hilo.join()
print(hilo.is_alive())
hilo.start()


"""
* Suposición:
El código se ejecuta sin problemas y se imprime "hola" en la consola,
luego se imprime "False" en la consola y finalmente se lanza una excepción
al intentar reiniciar el hilo.

* Acción real:
El código imprime "hola" en la consola, luego se imprime "False" en la consola.
"""