# ============================================
# EJEMPLO SIN LOCK — CONDICIÓN DE CARRERA
# ============================================
# Problema: dos hilos modifican la misma
# variable al mismo tiempo → resultado incorrecto
# ============================================

import threading

# Variable compartida
saldo = 100

def retirar():
    global saldo

    for i in range(1000):
        saldo = saldo - 1

# Creamos dos hilos que ejecutan la misma función
hilo1 = threading.Thread(target=retirar)
hilo2 = threading.Thread(target=retirar)

# Iniciamos los dos hilos
hilo1.start()
hilo2.start()

# Esperamos que ambos terminen
hilo1.join()
hilo2.join()

# Resultado esperado: 100 - 1000 - 1000 = -1900
# Resultado real: varía en cada ejecución

print(saldo)
# print(f"Saldo final: {saldo}")
#print(f"Saldo esperado: -1900")
#print(f"¿Son iguales? {saldo == -1900}")
