from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

# Conexion con Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# Crear una cita (con lock distribuido)
@app.post("/crear_cita")
def crear_cita():
    # nx=True solo crea la clave si no existe
    # ex=10 hace que el lock expire en 10 segundos
    lock = r.set("cita_10am", "ocupado", nx=True, ex=10)

    if not lock:
        raise HTTPException(status_code=400, detail="Cita ya reservada")

    return {"mensaje": "Cita reservada correctamente"}


# Ver el estado de la cita
@app.get("/ver_cita")
def ver_cita():
    cita = r.get("cita_10am")

    if cita is None:
        return {"mensaje": "No hay cita reservada"}

    return {"cita_10am": cita}


# Cancelar una cita (libera el lock)
@app.delete("/cancelar_cita")
def cancelar_cita():
    eliminado = r.delete("cita_10am")

    if eliminado == 0:
        raise HTTPException(status_code=404, detail="No hay cita para cancelar")

    return {"mensaje": "Cita cancelada"}