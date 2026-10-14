"""
PARCIAL 2 - Nivel 2 · Servidor concurrente

    python3 -m mensajeria.servidor            escucha en el puerto 8000
    python3 -m mensajeria.servidor 8050      o en el que se le diga

Tal como está, el servidor acepta conexiones y no hace nada con ellas. Falta
el hilo por conexión y la atención del cliente.

Requisitos:
  1. Un hilo por conexión. El hilo principal solo acepta.
  2. La primera trama del cliente es su nombre. El servidor responde "OK" y lo
     registra, o responde "ERROR: nombre en uso" y cierra la conexión.
  3. Cada trama siguiente se retransmite a todos los demás como
     "emisor: contenido".
  4. El envío va FUERA del lock: se copia la lista de destinatarios bajo el
     lock y se envía después.
  5. Una desconexión no tumba nada: si un cliente se va, con aviso o a la
     fuerza, su entrada se borra del registro y los demás siguen. Un
     destinatario al que ya no se puede enviar también se retira.
  6. SO_REUSEADDR y `with` para los sockets.

Se comprueba con:   python3 prueba_n2.py   (desde la carpeta parcial2/)

Nivel 3: copie este archivo, ya resuelto, a mensajeria/servidor_json.py y
trabaje sobre la copia.
"""

from __future__ import annotations

import socket
import sys
import threading

from mensajeria.protocolo import enviar_mensaje, recibir_mensaje
from mensajeria.registro import RegistroClientes

HOST = "127.0.0.1"
PUERTO = 8000


def retransmitir(registro: RegistroClientes, emisor: str, texto: str) -> None:
    """Envía "emisor: texto" a todos los conectados menos al emisor."""
    mensaje = f"{emisor}: {texto}"
    with registro.lock:
        destinatarios = [
            sock for nombre, sock in registro.clientes.items() if nombre != emisor
        ]
    for sock in destinatarios:
        try:
            enviar_mensaje(sock, mensaje)
        except Exception:
            with registro.lock:
                for nombre, s in list(registro.clientes.items()):
                    if s == sock:
                        del registro.clientes[nombre]
                        break


def atender(
    conexion: socket.socket, direccion: tuple[str, int], registro: RegistroClientes
) -> None:
    """Atiende a UN cliente, en su propio hilo, hasta que se desconecta."""
    nombre = recibir_mensaje(conexion)
    if nombre is None:
        conexion.close()
        return

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
            retransmitir(registro, nombre, trama)
    finally:
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
