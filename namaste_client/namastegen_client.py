import time
import requests

class NamastegenClientError(Exception):
    #When max retries have been used
    pass

class NamastegenClientTimeout(NamastegenClientError):
    #when timeout has been exceeded
    pass

class NamastegenClientJobError(NamastegenClientError):
    #if server returns error status
    pass

class NamastegenClient:
    def __init__(self, base_url, max_retries=5, timeout=60, backoff_factor=2):
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor

    def poll_status(self, callback=None):
        start_time = time.time()
        retries = 0
        while True:
            elapsed = time.time() - start_time
            if elapsed > self.timeout:
                #if job exceeds timeout, then break
                if callback:
                    callback("Timeout exceeded.")
                raise NamastegenClientTimeout("Timeout exceeded while waiting for job completion.")
            try:
                response = requests.get(f"{self.base_url}/status", timeout=5)
                response.raise_for_status() 
                result = response.json().get("result")

                if callback:
                    callback(f"Status: {result}")

                if result == "completed":
                    return "completed"
                elif result == "error":
                    raise NamastegenClientJobError("Job returned an error status.")            
            except requests.RequestException as e:
                # if failed, check untill max_retries
                if retries >= self.max_retries:
                    raise NamastegenClientError("Max retries reached while contacting server.") from e
            
            # Computing backoff delay
            delay = min((self.backoff_factor ** retries), self.timeout - elapsed)
            if callback:
                callback(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
            retries += 1
