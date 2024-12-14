from namaste_client.namastegen_client import NamastegenClient

def callback(message):
    print("Callback:", message)

client = NamastegenClient(base_url="http://localhost:8080", timeout=30)
status = client.poll_status(callback=callback)
print("Final status:", status)
