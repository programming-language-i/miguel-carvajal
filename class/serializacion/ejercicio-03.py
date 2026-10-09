import json

mensaje = {
    "emisor": "felipe",
    "contenido": "Hola, ¿cómo estás?",
    "etiquetas": ("a", "b")
}

texto = json.dumps(mensaje, ensure_ascii=False)
print(f"Texto serializado: {texto}")

copia = json.loads(texto)
print(f"Texto cargado: {copia}")

print("\n")

print(f"comparando el mensaje original con la copia: {mensaje == copia}")