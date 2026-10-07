import socket
import threading

HOST = "127.0.0.1"
PORT = 8000


def recibir_mensaje(conexion):
    while True:
        try:
            datos = conexion.recv(1024)
            if not datos:
                print("\nSe perdió la conexión con el servidor.")
                break
            print(f"\n{datos.decode()}")
            print("> ", end="", flush=True)
        except (ConnectionResetError, OSError):
            print("\nSe perdió la conexión con el servidor.")
            break


nombre = input("Escriba su nombre: ").strip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print("Conectado al servidor.")
    print("Escriba su mensaje y presione Enter para enviarlo. Escriba '0' para desconectarse.")

    hilo_receptor = threading.Thread(target=recibir_mensaje, args=(cliente,), daemon=True)
    hilo_receptor.start()

    while True:
        mensaje = input("> ")
        if mensaje.lower() == "0":
            print("Desconectando del servidor...")
            break

        cliente.sendall(f"{nombre}: {mensaje}".encode())