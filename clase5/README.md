# Clase 5 - Locks y Semáforos

---

## Problema

Cuando 50 usuarios intentan reservar 10 cursos
al mismo tiempo, dos usuarios pueden leer el mismo
valor simultáneamente y ambos descontar, generando
datos incorrectos. Esto se llama condición de carrera
(race condition).

---

## Parte 1 — Sin Lock

50 usuarios acceden al mismo recurso sin ningún
control. El resultado fue -40, cuando debería ser
0 o positivo. Esto demuestra la condición de carrera.

---

## Parte 2 — Solución con Lock

Con `with lock` solo un usuario puede reservar
a la vez. Los demás esperan su turno.
El resultado siempre fue 0. Correcto.

---

## Parte 3 — Solución con Semáforo

El semáforo permite máximo 3 reservas simultáneas.
Es más eficiente que el lock porque no obliga
a procesar de uno en uno, sino de tres en tres.
El resultado siempre fue 0. Correcto.

---

## Comparación de resultados

| Implementación | Resultado | ¿Correcto? |
|---|---|---|
| Sin Lock | -40 | ❌ |
| Con Lock | 0 | ✅ |
| Con Semáforo | 0 | ✅ |

---

## Conclusión

Sin control de concurrencia los datos terminan
incorrectos. El Lock garantiza exactitud procesando
de uno en uno. El Semáforo es más eficiente porque
permite N accesos simultáneos manteniendo el resultado
correcto.