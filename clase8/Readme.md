# Implementacion de sincronizacion distribuida con Redis

---

## Descripcion

Este proyecto implementa una API con FastAPI que usa Redis como coordinador para evitar reservas duplicadas en un sistema de citas medicas. Es la implementacion practica del diseño hecho en la Clase 7.

El sistema usa un lock distribuido en Redis para que solo un usuario pueda reservar un horario a la vez.

---

## Tecnologias usadas

- Python 3
- FastAPI
- Uvicorn
- Redis
- WSL Ubuntu

---

## Como ejecutarlo

### 1. Verificar que Redis este corriendo

```bash
redis-cli ping
```

Debe responder `PONG`.

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Levantar la API

```bash
uvicorn main:app --reload
```

Abrir en el navegador: http://127.0.0.1:8000/docs

---

## Endpoints

- `POST /crear_cita` - Crea una cita con lock distribuido
- `GET /ver_cita` - Consulta el estado de la cita
- `DELETE /cancelar_cita` - Cancela la cita y libera el lock

---

## Como funciona el lock

La linea clave del proyecto es:

```python
lock = r.set("cita_10am", "ocupado", nx=True, ex=10)
```

- `nx=True`: solo crea la clave si no existe (esto es lo que hace el lock)
- `ex=10`: la clave expira en 10 segundos para evitar que quede bloqueada si el sistema falla

---

## Prueba de concurrencia

El archivo `test_concurrencia.py` lanza 5 peticiones al mismo tiempo al endpoint `/crear_cita`.

Para ejecutarlo, con la API corriendo en otra terminal:

```bash
# Limpiar el lock previo
redis-cli DEL cita_10am

# Ejecutar la prueba
python3 test_concurrencia.py
```

Resultado esperado:
- 1 peticion debe ser exitosa (status 200)
- 4 peticiones deben ser rechazadas (status 400)

Esto demuestra que el lock distribuido funciona y solo un proceso pudo reservar la cita.

---

## Evidencias

Las capturas estan en la carpeta `evidencias/`:

- `01_redis_ping.png` - Redis corriendo
- `02_swagger.png` - Documentacion de la API
- `03_crear_cita_ok.png` - Primera peticion exitosa
- `04_crear_cita_error.png` - Segunda peticion rechazada
- `05_test_concurrencia.png` - Resultado de la prueba de concurrencia

---

## Conexion con sistemas distribuidos

### ¿Que problema se resolvio?

Se resolvio el problema de las reservas duplicadas. Cuando dos o mas usuarios intentan reservar el mismo horario al mismo tiempo, sin coordinacion los dos lo reservan y se genera duplicidad. En un sistema distribuido no se puede usar un lock local de Python porque cada servicio tiene su propia memoria y no comparten variables.

### ¿Como actua Redis como coordinador?

Redis funciona como una memoria compartida que todos los servicios pueden consultar. Cuando un servicio quiere reservar una cita, le pide a Redis que cree un lock con `nx=True`. Si el lock ya existe, Redis no lo crea de nuevo, asi que el segundo servicio sabe que el horario esta ocupado y devuelve un error. Ademas, el lock tiene tiempo de expiracion (`ex=10`) para que si un servicio falla, el lock se libere automaticamente y no quede bloqueado para siempre.