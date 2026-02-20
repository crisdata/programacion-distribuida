# Programación Distribuida - COTECNOVA 2026

---

## Clase 1 - Introducción a Sockets

### ¿Qué hice?
Creé mis primeros dos programas de comunicación distribuida:
- `servidor.py`: Un servidor que espera conexiones y envía mi nombre.
- `cliente.py`: Un cliente que se conecta al servidor y muestra el mensaje recibido.

### ¿Qué aprendí?
- Qué es un socket: un canal de comunicación entre dos procesos por red.
- La diferencia entre un proceso y un hilo:
  - **Proceso**: programa que se ejecuta de forma independiente con su propia memoria.
  - **Hilo (thread)**: tarea que corre dentro de un proceso, compartiendo su memoria.
- Qué es el modelo cliente-servidor:
  - El **servidor** escucha en un puerto esperando conexiones.
  - El **cliente** inicia la conexión hacia el servidor.
- Que siempre se debe iniciar el servidor ANTES que el cliente.

### Dificultades
- Al principio ejecuté el cliente antes que el servidor y obtuve el error `Connection refused`.
- Aprendí que ese error es normal en sistemas distribuidos y no es un error de código.

---

## Tecnologías usadas
- Python 3
- Módulo `socket` (incluido en Python)
- WSL (Ubuntu en Windows)
