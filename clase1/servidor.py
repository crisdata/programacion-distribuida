import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.1.1", 5000))
server.listen(1)

print("Servidor esperando conexión...")

conn, addr = server.accept()
print("Cliente conectado: ", addr)

nombre = "Cristian"
mensaje = f"Hola, soy {nombre}, bienvenido al servidor"
conn.sendall(mensaje.encode())

conn.close()
print("Conexión cerrada")
