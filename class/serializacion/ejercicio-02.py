# Estas librerías se utilizan para la serialización y deserialización
# de objetos en Python
import os
import pickle


# Ejemplo de serialización y deserialización con pickle
class Malisioso:
    # Definición de un método __reduce__ para ejecutar código malicioso
    # al deserializar
    def __reduce__(self):
        # El método __reduce__ devuelve una tupla que indica cómo reconstruir
        # el objeto durante la deserialización.
        return (os.system, ("echo 'Texto que se ejecuta en el sistema'",))

# deserealizacion de un menssaje   
carga = pickle.loads(pickle.dumps(Malisioso()))
print("Objeto malicioso deserializado:", carga)

"""
Este ejemplo muestra el funcionamento de la serialización y deserialización
con pickle, y cómo un objeto malicioso puede ejecutar código arbitrario
durante la deserialización.
"""
