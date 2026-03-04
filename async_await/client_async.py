import asyncio  # Librería para programación asíncrona
import time     # Librería para medir tiempo

async def main():
    # Abre conexión con el servidor
    reader, writer = await asyncio.open_connection("127.0.0.1", 5000)

    # Lee el nombre desde la terminal o desde el pipe (echo "Cliente_$i")
    name = input().strip()

    # Guarda el tiempo inicial
    start_time = time.time()

    # Envía el nombre al servidor
    writer.write(name.encode())

    # Asegura que el mensaje se envíe completamente
    await writer.drain()

    # Espera respuesta del servidor
    data = await reader.read(1024)

    # Guarda el tiempo final
    end_time = time.time()

    # Muestra la respuesta y el tiempo de atención
    print(f"[{name}] → {data.decode()}")
    print(f"[{name}] → Tiempo: {round(end_time - start_time, 2)}s")

    # Cierra la conexión limpiamente
    writer.close()
    await writer.wait_closed()

# Ejecuta el cliente
asyncio.run(main())