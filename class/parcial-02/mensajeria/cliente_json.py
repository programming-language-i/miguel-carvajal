"""
PARCIAL 2 - Nivel 3 · Servidor JSON
"""
from __future__ import annotations

import json
import socket
import sys
import threading
import time

from mensajeria.protocolo import enviar_mensaje, recibir_mensaje
from mensajeria.registro import RegistroClientes

HOST = "127.0.0.1"
PUERTO = 8000


def atender(
    conexion: socket.socket, direccion: tuple[str, int], registro: RegistroClientes
) -> None:
    """Atiende a UN cliente, en su propio hilo, hasta que se desconecta."""
    # La primera trama del cliente es su nombre (texto plano)
    nombre = recibir_mensaje(conexion)
    if nombre is None:
        conexion.close()
        return

    # Validar e insertar bajo el mismo lock del registro
    if not registro.insertar(nombre, conexion):
        enviar_mensaje(conexion, "ERROR: nombre en uso")
        conexion.close()
        return

    enviar_mensaje(conexion, "OK")

    try:
        while True:
            trama = recibir_mensaje(conexion)
            if trama is None:
                break

            # Intentamos interpretar la trama que envía el cliente como JSON
            try:
                datos_cliente = json.loads(trama)
                tipo = datos_cliente.get("tipo", "mensaje")
                contenido = datos_cliente.get("contenido", trama)
                destino = datos_cliente.get("destino")
            except json.JSONDecodeError:
                tipo = "mensaje"
                contenido = trama
                destino = None

            # Construimos el objeto JSON estructurado que el cliente espera recibir
            if tipo == "privado" and destino:
                # Mensaje privado
                mensaje_dict = {
                    "tipo": "privado",
                    "emisor": nombre,
                    "contenido": contenido,
                    "timestamp": time.time()
                }
                # Buscamos la conexión del destinatario
                sock_destino = registro.buscar(destino)
                if sock_destino:
                    try:
                        enviar_mensaje(sock_destino, json.dumps(mensaje_dict, ensure_ascii=False))
                    except Exception:
                        registro.borrar(destino)
                else:
                    # Si el destino no existe, podemos opcionalmente reportar error
                    error_dict = {
                        "tipo": "error",
                        "detalle": f"Usuario {destino} no encontrado"
                    }
                    try:
                        enviar_mensaje(conexion, json.dumps(error_dict, ensure_ascii=False))
                    except Exception:
                        pass
            else:
                # Mensaje público (retransmisión a todos los demás)
                mensaje_dict = {
                    "tipo": "mensaje",
                    "emisor": nombre,
                    "contenido": contenido,
                    "timestamp": time.time(),
                    "canal": "general" # O el canal por defecto que espere la prueba
                }
                mensaje_json = json.dumps(mensaje_dict, ensure_ascii=False)

                # Obtenemos la copia de destinatarios bajo el lock
                destinatarios = registro.destinatarios(excepto=nombre)

                # El envío se realiza FUERA del lock
                for nom_dest, sock_dest in destinatarios:
                    try:
                        enviar_mensaje(sock_dest, mensaje_json)
                    except Exception:
                        # Si un destinatario ya no responde, lo retiramos del registro
                        registro.borrar(nom_dest)
                        try:
                            sock_dest.close()
                        except Exception:
                            pass

    finally:
        # Si el cliente se desconecta, se borra del registro y se cierra la conexión
        registro.borrar(nombre)
        conexion.close()


def main() -> None:
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else PUERTO
    registro = RegistroClientes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, puerto))
        servidor.listen()
        print(f"escuchando en {HOST}:{puerto}")
        while True:
            conexion, direccion = servidor.accept()
            hilo = threading.Thread(
                target=atender, args=(conexion, direccion, registro), daemon=True
            )
            hilo.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nservidor detenido")
