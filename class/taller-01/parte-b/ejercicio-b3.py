### B3. Una excepción en el pool


from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


with ThreadPoolExecutor() as pool:
    futuro = pool.submit(dividir, 1, 0)
print("listo")


"""
* Suposición:
El cdodogo se ejecuta sin problemas y se imprime "listo" en la consola.

* Acción real:
el codigo imprime "listo" en la consola, pero la accion de 
"""
