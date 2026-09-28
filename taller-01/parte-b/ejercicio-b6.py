### B6. Estado por instancia y estado de clase


import threading


class Contador(threading.Thread):
    eventos = []  # noqa: RUF012

    def __init__(self, nombre):
        super().__init__(name=nombre)
        self.total = 0

    def run(self):
        for _ in range(3):
            self.total += 1
            self.eventos.append(self.name)


a, b = Contador("a"), Contador("b")
for h in (a, b):
    h.start()
for h in (a, b):
    h.join()
print(a.total, b.total, len(a.eventos))


"""
* Suposición:
El código se ejecuta sin problemas y se imprime "3 3 6" en la
consola, ya que cada hilo tiene su propio contador `total` y 
comparten la lista de eventos.

* Acción real:
El código imprime "3 3 6" en la consola, ya que cada hilo tiene
su propio contador `total` y comparten la lista de eventos.
"""