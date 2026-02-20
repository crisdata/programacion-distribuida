import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.1.1", 5000))

mensaje = client.recv(1024)
print("=" * 50)
print("MENSAJE RECIBIDO DESDE EL SERVIDOR:")
print(mensaje.decode())
print("=" * 50)

client.close()