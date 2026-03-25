# ============================================================
# prueba_hotel.py - Cliente de pruebas
# Ejercicio Independiente - Clase 6
# Concurrencia en Sistemas Distribuidos - COTECNOVA
# Profesor: Jhon James Cano Sánchez
# ============================================================

import asyncio
import httpx

# Semáforo que permite máximo 5 reservas simultáneas
# Esto evita saturar el servidor con demasiadas peticiones al tiempo
semaphore = asyncio.Semaphore(5)

async def cliente(numero, client):
    # Cada cliente debe adquirir el semáforo antes de hacer la petición
    async with semaphore:
        try:
            respuesta = await client.get("http://127.0.0.1:8000/reservar")
            datos = respuesta.json()

            # Mostrar progreso de cada cliente
            if datos["mensaje"] == "Reserva exitosa":
                print(f"Cliente {numero}: ¡Reservado! - Quedan {datos['habitaciones_disponibles']} habitaciones")
            else:
                print(f"Cliente {numero}: Sin disponibilidad")

        except Exception as e:
            print(f"Cliente {numero}: Error - {e}")

async def main():
    # Usar asyncio.gather() para ejecutar todos los clientes
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Simular 30 clientes intentando reservar al mismo tiempo
        await asyncio.gather(*[
            cliente(i + 1, client) for i in range(30)
        ])

    # Al final, mostrar cuántas habitaciones quedaron disponibles
    async with httpx.AsyncClient() as client:
        respuesta = await client.get("http://127.0.0.1:8000/estado")
        datos = respuesta.json()
        print(f"\n===== RESULTADO FINAL =====")
        print(f"Habitaciones disponibles: {datos['habitaciones_disponibles']}")
        print(f"===========================")

asyncio.run(main())