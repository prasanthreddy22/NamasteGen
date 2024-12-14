from flask import Flask, jsonify
import time
import threading
import random
import os

app = Flask(__name__)

JOB_DELAY = float(os.environ.get("JOB_DELAY", "10"))
ERROR_PROBABILITY = float(os.environ.get("ERROR_PROBABILITY", "0.1"))

status = {"result": "pending"}
start_time = time.time()

def simulation():
    # Keep doing untill job delay is not met
    while True:
        elapsed = time.time() - start_time
        if elapsed >= JOB_DELAY:
            # Random chance of error for simulation
            if random.random() < ERROR_PROBABILITY:
                status["result"] = "error"
            else:
                status["result"] = "completed"
            break
        time.sleep(1)

thread = threading.Thread(target=simulation)
thread.daemon = True
thread.start()

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
