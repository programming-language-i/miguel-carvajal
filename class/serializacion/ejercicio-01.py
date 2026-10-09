import pickle

mensaje = {
    "emisor": "felipe",
    "contenido": "Hola, ¿cómo estás?",
    "etiquetas": ("a", "b")
}

datos_serializados = pickle.dumps(mensaje)
print("Datos serializados:", datos_serializados)

print("\n")

copia = pickle.loads(datos_serializados)
print("Copia deserializada:", copia)
