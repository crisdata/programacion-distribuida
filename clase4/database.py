# ==========================
# IMPORTACIONES
# ==========================
import aiomysql  # Librería async para MySQL/MariaDB

# ==========================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "citas_db"
}

# ==========================
# FUNCIÓN DE CONEXIÓN
# ==========================
async def get_connection():
    """
    Crea una conexión async con la base de datos.
    Cada endpoint la llama cuando necesita consultar datos.
    """
    return await aiomysql.connect(**DB_CONFIG)
