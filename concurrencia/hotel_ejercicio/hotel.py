from fastapi import FastAPI
import asyncio

app = FastAPI()

# RECURSOS COMPARTIDOS
# El hotel tiene exactamente 8 habitaciones disponibles
habitaciones_disponibles = 8
# Lock para proteger la sección crítica y evitar condiciones de carrera
lock = asyncio.Lock()

# ENDPOINT: RESERVAR
# Permite reservar una habitación
@app.get("/reservar")
async def reservar():

    global habitaciones_disponibles

    # SECCIÓN CRÍTICA PROTEGIDA
    async with lock:    # Solo una petición entra aquí a la vez

        # Leer cuántas habitaciones hay disponibles
        disponibles = habitaciones_disponibles

        # Simular un proceso lento (como consultar una BD)
        await asyncio.sleep(0.2)

        # Si hay disponibilidad: reducir en 1 y devolver mensaje de éxito
        if disponibles > 0:
            habitaciones_disponibles = disponibles - 1
            return {
                "mensaje": "Reserva exitosa",
                "habitaciones_disponibles": habitaciones_disponibles
            }
        # Si no hay: devolver mensaje de error
        else:
            return {
                "mensaje": "No hay habitaciones disponibles",
                "habitaciones_disponibles": habitaciones_disponibles
            }

# ENDPOINT: ESTADO
# Consulta cuántas habitaciones quedan disponibles
@app.get("/estado")
async def estado():
    return {"habitaciones_disponibles": habitaciones_disponibles}

# ENDPOINT: REINICIAR
# Reinicia el contador a 8 habitaciones
@app.post("/reiniciar")
async def reiniciar():

    global habitaciones_disponibles

    async with lock:    # También se protege el reinicio
        valor_anterior = habitaciones_disponibles
        habitaciones_disponibles = 8

    return {
        "mensaje": "Hotel reiniciado",
        "valor_anterior": valor_anterior,
        "habitaciones_disponibles": habitaciones_disponibles
    }