from fastapi import FastAPI
import asyncio

app = FastAPI()    # Instancia de la aplicación

# RECURSOS COMPARTIDOS
contador = 0                # Variable global (recurso compartido)
lock = asyncio.Lock()       # Lock para proteger sección crítica

# ENDPOINT: INCREMENTAR
@app.get("/incrementar")
async def incrementar():

    global contador    # Indicamos que usaremos la variable global

    # SECCIÓN CRÍTICA PROTEGIDA
    async with lock:   # Solo una petición entra aquí a la vez

        valor_actual = contador    # Lectura del recurso compartido

        # Simulación de operación lenta (DB, API externa, etc.)
        await asyncio.sleep(0.1)

        contador = valor_actual + 1    # Escritura segura

    return {"contador": contador}

# ENDPOINT: VER CONTADOR
@app.get("/contador")
async def ver_contador():
    return {"contador": contador}

# ENDPOINT: RESET
@app.post("/reset")
async def resetear_contador():

    global contador

    async with lock:    # También se protege el reset
        valor_anterior = contador
        contador = 0

    return {
        "mensaje": "Contador reiniciado",
        "valor_anterior": valor_anterior,
        "contador_actual": contador
    }