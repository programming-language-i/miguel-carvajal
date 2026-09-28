### B5. Procesos y una lista global


import multiprocessing

resultados = []


def calcular(n):
    resultados.append(n * n)


if __name__ == "__main__":
    procesos = [multiprocessing.Process(target=calcular, args=(n,)) for n in range(4)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    print(resultados)


"""
* Suposición:
El código se ejecuta sin problemas y se imprime la lista [0, 1, 4, 9] 
en la consola.

* Acción real:
El código imprime una lista vacía en la consola, ya que cada proceso 
tiene su propio espacio de memoria y no comparte la lista global `resultados` 
con el proceso principal.    
"""