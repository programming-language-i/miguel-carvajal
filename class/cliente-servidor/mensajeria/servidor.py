import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

clientes = []
lock = threading.Lock()


def enviar_mensaje(mensaje, cliente_actual=None):
    print("Funcion de atención de mensajes")
    with lock:
        for cliente in clientes:
            if cliente != cliente_actual:
                try:
                   cliente.sendall(mensaje)
                except OSError:
                   print("Error al enviar mensaje. Cerrando conexión.")

def atender_cliente(conexion, direccion):
    print(f"Cliente conectado desde {direccion}")
    
    with lock:
        clientes.append(conexion)
        
    try:
        while True:
            datos = conexion.recv(1024)
            
            if not datos:
                print(f"Cliente {direccion} desconectado.")
                break
            
            print(f"Mensaje recibido de {direccion}: {datos.decode()}")
            enviar_mensaje(datos, conexion)
            
    except ConnectionResetError:
        print(f"Cliente {direccion} desconectado abruptamente.")
        
    finally:
        with lock:
            if conexion in clientes:
                clientes.remove(conexion)
            conexion.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    
    while True:
        conexion, direccion = servidor.accept()
        hilo_cliente = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo_cliente.start()