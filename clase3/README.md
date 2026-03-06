# Clase 3 — Microservicio Bancario con FastAPI

## Estructura del proyecto

```
clase3/
├── README.md
└── FastAPI/
    ├── main.py
    └── venv/
```

---

## Cómo ejecutar

```bash
# 1. Entrar a la carpeta del proyecto
cd FastAPI

# 2. Activar el entorno virtual
source venv/bin/activate

# 3. Levantar el servidor
python3 -m uvicorn main:app --reload
```

Acceder a la documentación automática en:
```
http://127.0.0.1:8000/docs
```

---

## Preguntas de reflexión

### ¿Es seguro usar variable global?

No es completamente seguro. Las variables globales `clientes` y `total_creados` son accedidas y modificadas por todos los endpoints. Si dos peticiones llegan al servidor exactamente al mismo tiempo, ambas podrían intentar modificar la misma variable simultáneamente, generando datos incorrectos o inconsistentes. Para este ejercicio académico funciona sin problema, pero no es una práctica recomendada para entornos reales.

### ¿Dónde aparece el recurso compartido?

El recurso compartido aparece en dos variables globales:

- **`clientes`**: lista que almacena todos los clientes en memoria RAM. Es leída y modificada por los endpoints POST, GET, PUT y DELETE.
- **`total_creados`**: contador entero que registra cuántos clientes se han creado históricamente. Es modificado cada vez que se llama al endpoint POST.

Ambas variables son compartidas entre todas las peticiones que recibe el servidor de forma concurrente.

### ¿Se debería usar lock en producción?

Sí. En un entorno de producción donde múltiples usuarios pueden hacer peticiones simultáneas, se debería usar un mecanismo de control de acceso como `asyncio.Lock()`. Un lock garantiza que solo una petición a la vez pueda modificar las variables compartidas, evitando las condiciones de carrera (race conditions) que pueden causar errores difíciles de detectar. Sin lock, existe el riesgo de que dos clientes queden con el mismo ID o que el contador no refleje el valor real.