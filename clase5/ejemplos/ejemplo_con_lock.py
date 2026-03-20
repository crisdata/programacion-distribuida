# ============================================
# EJEMPLO CON LOCK — SOLUCIÓN
# ============================================
# Solución: con lock solo un hilo puede entrar
# a la sección crítica a la vez
# ============================================

import threading
import time

# Variable compartida
saldo = 100

# Creamos el lock
lock = threading.Lock()

def retirar(nombre):
    global saldo
    
    for i in range(5):

        with lock:  # ← solo un hilo entra aquí a la vez
            valor_leido = saldo
            time.sleep(0.01)
            saldo = valor_leido - 10
            print(f"{nombre} retiró 10 → saldo: {saldo}")

# Creamos dos hilos
hilo1 = threading.Thread(target=retirar, args=("Hilo-A",))
hilo2 = threading.Thread(target=retirar, args=("Hilo-B",))

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

# Resultado esperado: 100 - (5*10) - (5*10) = 0
print(f"\nSaldo final:    {saldo}")
print(f"Saldo esperado: 0")
print(f"¿Resultado correcto? {saldo == 0}")