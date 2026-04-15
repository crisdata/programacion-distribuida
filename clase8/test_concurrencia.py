import requests
import threading

URL = "http://127.0.0.1:8000/crear_cita"

resultados = []


def hacer_peticion(numero):
    respuesta = requests.post(URL)
    resultados.append({
        "peticion": numero,
        "status": respuesta.status_code,
        "respuesta": respuesta.json()
    })


# Lanzar 5 peticiones al mismo tiempo
hilos = []
for i in range(1, 6):
    h = threading.Thread(target=hacer_peticion, args=(i,))
    hilos.append(h)
    h.start()

# Esperar a que terminen
for h in hilos:
    h.join()

# Mostrar resultados
print("Resultado de las peticiones:")
for r in resultados:
    print(f"Peticion {r['peticion']} - Status: {r['status']} - {r['respuesta']}")