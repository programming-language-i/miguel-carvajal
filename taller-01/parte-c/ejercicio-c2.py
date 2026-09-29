## Parte C — Encontrar el error
"""
Cada fragmento falla o no hace lo que su autor cree. Para cada uno:
**(1)** qué pasa al ejecutarlo
**(2)** por qué
**(3)** la corrección mínima.
"""


### C2. Tres tareas "concurrentes"


import threading
import time


class Tarea(threading.Thread):
    def start(self):
        time.sleep(1)
        print(self.name, "lista")


inicio = time.perf_counter()
tareas = [Tarea(name=f"t{i}") for i in range(3)]
for t in tareas:
    t.start()
print(f"{time.perf_counter() - inicio:.1f} s")
for t in tareas:
    t.join()



"""
- (1) Qué pasa al ejecutarlo?
R// El programa imprime "t0 lista", "t1 lista" y "t2 lista" después de aproximadamente 1 segundo, y luego imprime el tiempo total transcurrido, que es alrededor de 1.0 segundos.

- (2) Por qué?
R// El programa crea tres instancias de la clase `Tarea`, que hereda de `threading.Thread`. Cada instancia de `Tarea` tiene un método `start` que duerme durante 1 segundo y luego imprime el nombre de la tarea. Cuando se llama a `start()` en cada tarea, se ejecuta el método `start` de la clase `Tarea`, lo que provoca que cada tarea duerma durante 1 segundo antes de imprimir su nombre. Como las tareas se ejecutan concurrentemente, todas terminan aproximadamente al mismo tiempo, resultando en un tiempo total de ejecución cercano a 1 segundo.

- (3) La corrección mínima:
R// La corrección mínima es cambiar el nombre del método `start` en la clase `Tarea` a otro nombre, como `run`, para que no sobrescriba el método `start` de la clase base `threading.Thread`. Esto permitirá que las tareas se ejecuten correctamente en hilos separados. El código corregido sería:

```python
class Tarea(threading.Thread):
    def run(self):
        time.sleep(1)
        print(self.name, "lista")
```
"""
