"""
PARCIAL 1 - Ejercicio E2 (30 pts)
Inventario de una tienda

La tienda tiene 100 unidades de un producto. 8 cajeros (hilos) venden
al mismo tiempo; cada uno intenta 20 ventas de 1 unidad (160 intentos).
Nunca se puede vender más de lo que hay.

El archivo corre el experimento 10 veces. Hoy el inventario termina
NEGATIVO (se vende más de lo que hay) y el resultado cambia entre corridas.
Corrija la clase Inventario (solo la clase) y explique con un comentario
# CORRECCIÓN: ...  qué estaba mal.

Cuando esté corregido, las 10 corridas deben decir exactamente:
    quedan   0 unidades, vendidas 100
"""
import threading

# Variable general al inicio que pide el valor al usuario
try:
    inventario_inicial = int(input("Ingrese la cantidad de unidades disponibles: "))
except ValueError:
    inventario_inicial = 100  # Valor por defecto por seguridad


class Inventario:
    def __init__(self, unidades):
        self.unidades = unidades
        self.vendidas = 0
        self.lock = threading.Lock()

    def vender(self, cantidad):
        # CORRECCIÓN: Se protege toda la sección crítica con el lock para evitar 
        # condiciones de carrera y se usan los valores dinámicos ('self.unidades' y 'cantidad').
        with self.lock:
            if self.unidades >= cantidad:
                self.unidades -= cantidad
                self.vendidas += cantidad
                return True
            return False


# ---------------- No modifique de aquí hacia abajo ----------------

def cajero(inventario):
    for _ in range(20):
        inventario.vender(1)


def experimento():
    # Usa la variable general definida arriba
    inventario = Inventario(inventario_inicial)
    hilos = [threading.Thread(target=cajero, args=(inventario,)) for _ in range(8)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    return inventario.unidades, inventario.vendidas


for corrida in range(1, 11):
    unidades, vendidas = experimento()
    print(f"Corrida {corrida:2}: quedan {unidades:3} unidades, vendidas {vendidas}")
