# ============================================
# EJEMPLO SEMÁFORO — EXACTO DEL PROFESOR
# ============================================
# Solo 2 usuarios pueden imprimir al mismo
# tiempo, aunque haya 5 intentando hacerlo.
# ============================================

import threading
import time

# Creamos el semáforo con valor 2
# Eso significa: máximo 2 hilos simultáneos
# Si un tercero intenta entrar, espera afuera
sem = threading.Semaphore(2)

def imprimir(nombre):

    # acquire() = "pido permiso para entrar"
    # Si hay cupo disponible → entra de inmediato
    # Si no hay cupo → el hilo se queda esperando
    # aquí hasta que alguien haga release()
    sem.acquire()

    print(nombre, "está imprimiendo")

    # Simulamos que imprimir tarda 3 segundos
    # Durante ese tiempo el semáforo sigue ocupado
    time.sleep(3)

    print(nombre, "terminó")

    # release() = "libero mi lugar"
    # Esto le avisa al semáforo que hay un cupo
    # libre, y el siguiente hilo que estaba
    # esperando puede entrar
    sem.release()

# Creamos 5 hilos directamente en el for
# tal cual lo muestra el profesor
for i in range(5):
    threading.Thread(
        target=imprimir,
        args=(f"Usuario {i}",)
    ).start()