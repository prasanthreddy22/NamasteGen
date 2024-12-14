import asyncio
from namaste_client.heygen_client import HeygenClient

async def my_callback(message):
    print("Callback:", message)

async def main():
    client = HeygenClient("http://localhost:8080", timeout=30)
    result = await client.poll_status(callback=my_callback)
    print("Final result:", result)

asyncio.run(main())
