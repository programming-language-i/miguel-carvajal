## Parte C — Encontrar el error
"""
Cada fragmento falla o no hace lo que su autor cree. Para cada uno:
**(1)** qué pasa al ejecutarlo
**(2)** por qué
**(3)** la corrección mínima.
"""


### C3. Un pool de procesos sin guarda


from concurrent.futures import ProcessPoolExecutor


def cuadrado(n):
    return n * n


with ProcessPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(cuadrado, range(4))))



"""
- (1) Qué pasa al ejecutarlo?
R// El programa lanza un error de tipo `AttributeError: Can't pickle local
object 'cuadrado'`.

- (2) Por qué?
R// Porque la función `cuadrado` está definida en el ámbito local del script
y no puede ser serializada (pickled) para ser enviada a los procesos del pool.
Los procesos en Python requieren que las funciones y objetos que se pasan entre
ellos sean serializables, y las funciones definidas localmente no cumplen con este
requisito.

- (3) La corrección mínima:
R// La corrección mínima es definir la función `cuadrado` en el ámbito global del
módulo, fuera de cualquier clase o función. Esto permitirá que la función sea
serializable y pueda ser utilizada por los procesos del pool. El código corregido
sería:

```python
def cuadrado(n):
    return n * n
```

"""
