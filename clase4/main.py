# ==========================
# IMPORTACIONES
# ==========================
from fastapi import FastAPI, HTTPException
import asyncio
from database import get_connection

app = FastAPI()

# ==========================
# 1. CREAR CITA
# POST /citas
# Sistema base del profesor
# ==========================
@app.post("/citas")
async def crear_cita(paciente: str, fecha: str):
    """Crea una nueva cita. Simula delay de 2 segundos."""
    await asyncio.sleep(2)  # Simulación proceso lento

    conn = await get_connection()
    cursor = await conn.cursor()

    query = """
    INSERT INTO citas (paciente, fecha, estado)
    VALUES (%s, %s, %s)
    """
    await cursor.execute(query, (paciente, fecha, "activa"))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "Cita creada correctamente"}


# ==========================
# 2. LISTAR CITAS ACTIVAS
# GET /citas/activas
# Actividad en clase
# IMPORTANTE: va ANTES de /citas/{paciente}
# ==========================
@app.get("/citas/activas")
async def listar_citas_activas():
    """Retorna solo las citas con estado activa."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE estado='activa'"
    await cursor.execute(query)
    citas = await cursor.fetchall()

    await cursor.close()
    conn.close()

    return citas


# ==========================
# 3. CONTAR CITAS
# GET /citas/count
# Actividad en clase
# IMPORTANTE: va ANTES de /citas/{paciente}
# ==========================
@app.get("/citas/count")
async def contar_citas():
    """Retorna el total de citas registradas."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT COUNT(*) FROM citas"
    await cursor.execute(query)
    resultado = await cursor.fetchone()

    await cursor.close()
    conn.close()

    return {"total_citas": resultado[0]}


# ==========================
# 4. LISTAR CITAS POR FECHA
# GET /citas/fecha/{fecha}
# Actividad independiente
# IMPORTANTE: va ANTES de /citas/{paciente}
# ==========================
@app.get("/citas/fecha/{fecha}")
async def listar_citas_por_fecha(fecha: str):
    """Retorna todas las citas de una fecha específica."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE fecha=%s"
    await cursor.execute(query, (fecha,))
    citas = await cursor.fetchall()

    await cursor.close()
    conn.close()

    if not citas:
        raise HTTPException(
            status_code=404,
            detail="No hay citas para esa fecha"
        )

    return citas


# ==========================
# 5. LISTAR TODAS LAS CITAS
# GET /citas
# Sistema base del profesor
# ==========================
@app.get("/citas")
async def listar_citas():
    """Retorna todas las citas sin filtro."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas"
    await cursor.execute(query)
    citas = await cursor.fetchall()

    await cursor.close()
    conn.close()

    return citas


# ==========================
# 6. BUSCAR CITA POR PACIENTE
# GET /citas/{paciente}
# Sistema base del profesor
# IMPORTANTE: va DESPUÉS de las rutas fijas
# ==========================
@app.get("/citas/{paciente}")
async def buscar_cita(paciente: str):
    """Busca citas por nombre de paciente."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "SELECT * FROM citas WHERE paciente=%s"
    await cursor.execute(query, (paciente,))
    cita = await cursor.fetchone()

    await cursor.close()
    conn.close()

    if not cita:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    return cita


# ==========================
# 7. REACTIVAR CITA CANCELADA
# PUT /citas/reactivar/{id}
# Actividad en clase
# ==========================
@app.put("/citas/reactivar/{id}")
async def reactivar_cita(id: int):
    """Cambia el estado de una cita cancelada a activa."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "UPDATE citas SET estado='activa' WHERE id=%s"
    await cursor.execute(query, (id,))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "Cita reactivada correctamente"}


# ==========================
# 8. ACTUALIZAR FECHA DE CITA
# PUT /citas/{id}
# Actividad independiente
# ==========================
@app.put("/citas/{id}")
async def actualizar_fecha(id: int, fecha: str):
    """Actualiza la fecha de una cita existente."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "UPDATE citas SET fecha=%s WHERE id=%s"
    await cursor.execute(query, (fecha, id))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "Fecha actualizada correctamente"}


# ==========================
# 9. ELIMINAR CITA
# DELETE /citas/{id}
# Actividad independiente
# ==========================
@app.delete("/citas/{id}")
async def eliminar_cita(id: int):
    """Elimina físicamente una cita de la base de datos."""
    conn = await get_connection()
    cursor = await conn.cursor()

    query = "DELETE FROM citas WHERE id=%s"
    await cursor.execute(query, (id,))
    await conn.commit()

    await cursor.close()
    conn.close()

    return {"mensaje": "Cita eliminada correctamente"}
