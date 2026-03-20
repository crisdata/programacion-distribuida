# ============================================
# ACTIVIDAD EN CLASE — RESERVA DE ASIENTOS
# ============================================

import threading
import time

# ── PARTE 1: SIN LOCK (el problema) ─────────

# Paso 1: variable global
asientos = 10

# Paso 2: función de reserva
def reservar():
    global asientos
    if asientos > 0:
        time.sleep(0.01)  # simula proceso real
        asientos -= 1

# Paso 3: crear múltiples hilos
for i in range(50):
    threading.Thread(target=reservar).start()

time.sleep(1)  # esperamos que terminen todos
print("=" * 40)
print("PARTE 1 — SIN LOCK")
print(f"Asientos finales:    {asientos}")
print(f"¿Puede ser negativo? {asientos < 0}")
print("=" * 40)

# ── PARTE 2: CON LOCK (Paso 4 del profesor) ──

asientos = 10
lock = threading.Lock()

def reservar_seguro():
    global asientos
    with lock:          # protege la sección crítica
        if asientos > 0:
            asientos -= 1

for i in range(50):
    threading.Thread(target=reservar_seguro).start()

time.sleep(1)
print("PARTE 2 — CON LOCK")
print(f"Asientos finales:    {asientos}")
print(f"¿Resultado correcto? {asientos == 0}")
print("=" * 40)