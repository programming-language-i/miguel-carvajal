"""
PARCIAL 2 - Nivel 2 (20 pts) · Registro de clientes

Quién está conectado: un dict con el nombre como clave, protegido con UN
threading.Lock. Lo usan a la vez todos los hilos del servidor.

Aquí solo están las firmas: escriba el cuerpo de los cinco métodos.

Requisitos:
  1. insertar devuelve False si el nombre ya está en uso. Verificar e insertar
     ocurren bajo el MISMO lock.
  2. buscar devuelve la conexión de ese nombre, o None si no está.
  3. borrar quita la entrada. Borrar un nombre que ya no está no es un error.
  4. destinatarios devuelve UNA COPIA, hecha dentro del lock: la lista de
     (nombre, conexion) de todos menos `excepto`.
"""
from __future__ import annotations

import socket
import threading


class RegistroClientes:
    def __init__(self) -> None:
        self.clientes = {}
        self.lock = threading.Lock()

    def insertar(self, nombre: str, conexion: socket.socket) -> bool:
        # Completar
        with self.lock:
            if nombre in self.clientes:
                return False
            self.clientes[nombre] = conexion
            return True

    def buscar(self, nombre: str) -> socket.socket | None:
        # Completar
        with self.lock:
            return self.clientes.get(nombre, None)

    def borrar(self, nombre: str) -> None:
        # Completar
        with self.lock:
            if nombre in self.clientes:
                del self.clientes[nombre]

    def destinatarios(self, excepto: str) -> list[tuple[str, socket.socket]]:
        # Completar
        with self.lock:
            return [(nombre, sock) for nombre, sock in self.clientes.items() if nombre != excepto]
