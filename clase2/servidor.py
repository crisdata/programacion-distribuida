import socket
import threading
import time

contador_clientes = 0
lock = threading.Lock()


def handle_client(conn, addr):
    global contador_clientes

    print(f"Cliente conectado desde: {addr}")

    try:
        with lock:
            contador_clientes += 1
            numero = contador_clientes

        print(f"Contador de clientes: {numero} atentido desde {addr}")
        student_name = conn.recv(1024).decode()

        # Simulación de atención bancaria
        time.sleep(5)

        response = f"Hola {student_name}, fuiste el cliente #{numero} atendido por un servidor concurrente!"
        conn.sendall(response.encode())
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexión cerrada con {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para evitar el error "Address already in use" al reiniciar el servidor en WSL
server.bind(("0.0.0.0", 5000))
server.listen()

print("Servidor concurrente escuchando...")

while True:
    conn, addr = server.accept()

    # Create a thread per client
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
