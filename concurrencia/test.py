import asyncio
import httpx

# Controla máximo 10 peticiones concurrentes
semaphore = asyncio.Semaphore(10)

async def peticion(client):
    async with semaphore:
        try:
            await client.get("http://127.0.0.1:8000/incrementar")
        except Exception as e:
            print("Error:", e)

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        await asyncio.gather(*[
            peticion(client) for _ in range(100)
        ])

asyncio.run(main())