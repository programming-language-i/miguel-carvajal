## Parte C — Encontrar el error
"""
Cada fragmento falla o no hace lo que su autor cree. Para cada uno:
**(1)** qué pasa al ejecutarlo
**(2)** por qué
**(3)** la corrección mínima.
"""

### C1. Descarga por herencia


import threading


class Descarga(threading.Thread):
    def __init__(self, archivo):
        self.archivo = archivo

    def run(self):
        print("descargando", self.archivo)


Descarga("a.zip").start()


"""
- (1) Qué pasa al ejecutarlo?
R// El programa lanza un error de tipo `TypeError: super(type, obj): 
obj must be an instance or subtype of type`.

- (2) Por qué?
R// Porque la clase `Descarga` hereda de `threading.Thread`, y en el método
`__init__` no se llama al constructor de la clase base. Esto significa que 
la inicialización de la clase base no se realiza correctamente, lo que provoca
un error cuando se intenta iniciar el hilo.

- (3) La corrección mínima:
R// La corrección mínima es llamar al constructor de la clase base
`threading.Thread` dentro del método `__init__` de la clase `Descarga`.
Esto se puede hacer utilizando `super().__init__()`.

el código corregido sería:
```python
class Descarga(threading.Thread):
    def __init__(self, archivo):
        super().__init__()  # Llamada al constructor de la clase base
        self.archivo = archivo
        self.start()

    def run(self):
        print("descargando", self.archivo)
    
Descarga("a.zip")
```

"""
