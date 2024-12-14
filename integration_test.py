import subprocess
import time
import os
import pytest
from namaste_client.namastegen_client import NamastegenClient, NamastegenClientTimeout, NamastegenClientJobError

@pytest.fixture(scope="module")
def test_server():
    # Giving base environments
    # setting error probability for server
    env = os.environ.copy()
    env["JOB_DELAY"] = "15"        # The job completes after 5 seconds
    env["ERROR_PROBABILITY"] = "0.2"  # 20% chance of error

    # Starting server
    server_proc = subprocess.Popen(["python", "server/server.py"], env=env)
    time.sleep(2)

    yield server_proc

    # kill the server
    server_proc.terminate()
    server_proc.wait()


def test_poll_status(test_server):
    client = NamastegenClient(base_url="http://localhost:8080", max_retries=5, timeout=30)

    def status_callback(message):
        print("[TEST CALLBACK]", message)

    try:
        final_status = client.poll_status(callback=status_callback)
        print("[TEST] Final status:", final_status)
        assert final_status == "completed"
    except NamastegenClientTimeout:
        print("[TEST] Timed out waiting for job completion.")
    except NamastegenClientJobError:
        print("[TEST] The job ended in error.")
