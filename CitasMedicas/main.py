# ================================
# IMPORTACIONES
# ================================

from fastapi import FastAPI, HTTPException  # FastAPI y manejo de errores
from typing import List                     # Para tipar respuestas como lista
import asyncio                              # Para el delay asíncrono

# ================================
# CREACIÓN DE LA APLICACIÓN
# ================================

app = FastAPI()  # Instancia principal de la API

# ================================
# BASE DE DATOS SIMULADA EN MEMORIA
# ================================

# Lista global que almacena todas las citas en RAM
# Cada cita es un diccionario con: id, paciente, medico, fecha, estado
citas = []

# ================================
# ENDPOINT RAÍZ — GET /
# ================================

@app.get("/")
async def home():
    return {"mensaje": "Sistema de Citas Médicas funcionando"}


# ================================
# CREAR CITA — POST /citas
# ================================

@app.post("/citas")
async def crear_cita(paciente: str, medico: str, fecha: str):
    """
    Crea una nueva cita médica.
    - paciente: nombre del paciente (no puede estar vacío)
    - medico: nombre del médico (no puede estar vacío)
    - fecha: fecha de la cita, ejemplo: 2026-03-10 (no puede estar vacía)
    - Simula delay de 2 segundos como operación de registro
    """

    # Validación: ningún campo puede estar vacío
    if not paciente.strip():
        raise HTTPException(status_code=400, detail="El nombre del paciente no puede estar vacío")

    if not medico.strip():
        raise HTTPException(status_code=400, detail="El nombre del médico no puede estar vacío")

    if not fecha.strip():
        raise HTTPException(status_code=400, detail="La fecha no puede estar vacía")

    # Delay asíncrono de 2 segundos — simula el proceso de registro
    await asyncio.sleep(2)

    # Construir el diccionario de la cita
    cita = {
        "id": len(citas) + 1,        # ID automático basado en cuántas citas hay
        "paciente": paciente.strip(), # Nombre del paciente sin espacios extra
        "medico": medico.strip(),     # Nombre del médico sin espacios extra
        "fecha": fecha.strip(),       # Fecha de la cita
        "estado": "activa"            # Estado inicial siempre es "activa"
    }

    citas.append(cita)  # Guardar en la lista global

    return {"mensaje": "Cita creada exitosamente", "cita": cita}


# ================================
# LISTAR CITAS — GET /citas
# ================================

@app.get("/citas", response_model=List[dict])
async def listar_citas():
    """
    Retorna todas las citas registradas (activas y canceladas).
    """
    return citas


# ================================
# BUSCAR CITA POR PACIENTE — GET /citas/paciente/{nombre}
# ================================

@app.get("/citas/paciente/{nombre_paciente}")
async def buscar_por_paciente(nombre_paciente: str):
    """
    Busca y retorna todas las citas que pertenecen a un paciente.
    - Un paciente puede tener más de una cita, por eso retornamos una lista
    """

    # Lista vacía donde iremos guardando las citas que coincidan
    resultados = []

    # Recorremos todas las citas una por una
    for cita in citas:
        # .lower() convierte a minúsculas para que "Juan" y "juan" sean lo mismo
        if cita["paciente"].lower() == nombre_paciente.lower():
            resultados.append(cita)  # Si coincide, la agregamos a resultados

    # Si la lista de resultados está vacía, el paciente no tiene citas registradas
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron citas para ese paciente")

    return resultados  # Retorna la lista de citas encontradas


# ================================
# CANCELAR CITA — DELETE /citas/{id}
# ================================

@app.delete("/citas/{cita_id}")
async def cancelar_cita(cita_id: int):
    """
    Cancela una cita cambiando su estado a "cancelada".
    No elimina la cita de la lista — solo cambia el estado.
    Esto es más realista: en sistemas médicos reales se guarda el historial.
    """

    for cita in citas:
        if cita["id"] == cita_id:

            # Verificar que la cita no esté ya cancelada
            if cita["estado"] == "cancelada":
                raise HTTPException(status_code=400, detail="La cita ya está cancelada")

            cita["estado"] = "cancelada"  # Cambiamos el estado en lugar de borrar
            return {"mensaje": f"Cita {cita_id} cancelada correctamente", "cita": cita}

    raise HTTPException(status_code=404, detail="Cita no encontrada")