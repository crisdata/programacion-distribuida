# ============================================
# ACTIVIDAD INDEPENDIENTE
# Sistema de reservas concurrente
# ============================================
# Simular: 50 usuarios que reservan 10 cursos
# ============================================

import threading
import time

# ============================================
# PARTE 1 — SIN LOCK (el problema)
# ============================================

# Variable global: solo hay 10 cursos disponibles
cursos = 10

def reservar_curso():
    global cursos
    # Si hay cursos disponibles, reserva uno
    if cursos > 0:
        # time.sleep simula el tiempo real de
        # procesamiento. En ese instante otros
        # hilos entran y leen el mismo valor
        time.sleep(0.01)
        cursos -= 1  # ← sección crítica sin proteger

# 50 usuarios intentan reservar al mismo tiempo
for i in range(50):
    threading.Thread(target=reservar_curso).start()

time.sleep(2)  # esperamos que todos los hilos terminen

print("=" * 40)
print("PARTE 1 — SIN LOCK")
print(f"Cursos disponibles: {cursos}")
print(f"Resultado esperado: 0 o positivo")
print(f"¿Hay problema?      {cursos < 0}")
print("=" * 40)

# ============================================
# PARTE 2 — CON LOCK (solución)
# ============================================

# Reiniciamos los cursos para la segunda prueba
cursos = 10

# El lock garantiza que solo un hilo entra
# a la sección crítica a la vez
lock = threading.Lock()

def reservar_curso_lock():
    global cursos
    # with lock: solo un usuario puede reservar
    # a la vez, los demás esperan su turno
    with lock:
        if cursos > 0:
            cursos -= 1  # ← sección crítica protegida

# 50 usuarios intentan reservar al mismo tiempo
for i in range(50):
    threading.Thread(target=reservar_curso_lock).start()

time.sleep(2)

print("PARTE 2 — CON LOCK")
print(f"Cursos disponibles: {cursos}")
print(f"Resultado esperado: 0")
print(f"¿Resultado correcto? {cursos == 0}")
print("=" * 40)

# ============================================
# PARTE 3 — CON SEMÁFORO
# ============================================
# Diferencia con Lock:
# Lock     → solo 1 usuario reserva a la vez
# Semáforo → hasta N usuarios reservan a la vez
# Aquí: máximo 3 reservas simultáneas
# ============================================

# Reiniciamos los cursos para la tercera prueba
cursos = 10

# Semáforo con valor 3 = máximo 3 simultáneos
sem = threading.Semaphore(3)

def reservar_curso_semaforo(numero):
    global cursos

    # acquire() = pido permiso para entrar
    # Si hay cupo → entra de inmediato
    # Si no hay cupo → espera hasta que alguien salga
    sem.acquire()

    if cursos > 0:
        print(f"Usuario {numero} reservando... cursos: {cursos}")
        cursos -= 1

    # release() = libero mi lugar
    # Esto permite que el siguiente usuario entre
    sem.release()

# 50 usuarios intentan reservar al mismo tiempo
for i in range(50):
    threading.Thread(
        target=reservar_curso_semaforo,
        args=(i,)
    ).start()

time.sleep(2)

print("=" * 40)
print("PARTE 3 — CON SEMÁFORO (máx 3 simultáneos)")
print(f"Cursos disponibles: {cursos}")
print(f"Resultado esperado: 0")
print(f"¿Resultado correcto? {cursos == 0}")
print("=" * 40)