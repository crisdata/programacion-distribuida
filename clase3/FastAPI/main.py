#IMPORTACIONES

from fastapi import FastAPI, HTTPException   # FastAPI + manejo de errores HTTP
import asyncio                               # Para simular delays asíncronos
from typing import List                      # Para indicar que la respuesta es una lista


#Creación de la aplicación

app = FastAPI() #Objeto principal de la API (Instancia del framework)

#BASE DE DATOS SIMULADA (En memoria)

clientes = []       # Lista global donde se guardan los clientes
total_creados = 0   # Contador global — cuántos clientes se han creado en total

#PASO 3 ENPOINT RAIZ
@app.get("/")
def home():
    # Retorna un mensaje simple para verificar que el servidor está vivo
    return {"mensaje": "API del Banco funcionando"}

#PASO 4 CREAR CLIENTE (POST)
@app.post("/clientes")
async def crear_cliente(nombre: str):
    # Requisito 3 — Validación: no permitir nombre vacío
    # .strip() elimina espacios en blanco al inicio y al final
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    # Requisito 5 — Delay asíncrono de 3 segundos
    # Simula una operación pesada sin bloquear el servidor
    await asyncio.sleep(3)

    # Requisito 4 — Contador global de clientes creados
    # "global" es necesario para modificar la variable fuera de la función
    global total_creados
    total_creados += 1

    # Construir el cliente como diccionario
    cliente = {
        "id": len(clientes) + 1,
        "nombre": nombre.strip()
    }

    clientes.append(cliente)  # Agregar a la lista global

    return {"cliente_creado": cliente, "total_creados": total_creados}


#PASO 5 LISTAR CLIENTES (GET)
@app.get("/clientes", response_model=List[dict])  #Define tipo de respuesta
def listar_clientes():
    return clientes  #Devuelve lista completa

#PASO 6 OBTENER CLIENTE POR ID
@app.get("/clientes/{cliente_id}")   #Ruta con parametro dinamico
def obtener_cliente(cliente_id: int): #Tipo entero
    for cliente in clientes:  #Recorre lista
        if cliente["id"] == cliente_id:
            return cliente  #Retorna si encuentra
        
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# ================================
# REQUISITO 2 — PUT /clientes/{id}
# Actualizar nombre de un cliente
# ================================

@app.put("/clientes/{cliente_id}")
async def actualizar_cliente(cliente_id: int, nuevo_nombre: str):

    # Validación: el nuevo nombre tampoco puede estar vacío
    if not nuevo_nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = nuevo_nombre.strip()
            return {"mensaje": "Cliente actualizado", "cliente": cliente}

    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# ================================
# REQUISITO 1 — DELETE /clientes/{id}
# Eliminar un cliente por ID
# ================================

@app.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):

    # enumerate() nos da el índice y el elemento al mismo tiempo
    for indice, cliente in enumerate(clientes):
        if cliente["id"] == cliente_id:
            clientes.pop(indice)  # Elimina el elemento en esa posición
            return {"mensaje": f"Cliente {cliente_id} eliminado correctamente"}

    raise HTTPException(status_code=404, detail="Cliente no encontrado")