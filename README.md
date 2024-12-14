# Server and Client Example

## Overview

This repository demonstrates a polling client for a simulated video translation job. It does:

- Implement exponential backoff to reduce load.
- Provide callbacks for real-time updates.
- Prevents indefinite waits and excessive polling

## Steps to Run Test

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

2. **Running Tests:**
   ```bash
   pytest -s integration_test.py

## Steps to Run Library

1. **Import Library:**
   ```bash
   import NamastegenClient

2. **Initializing Client:**
   ```bash
   NamastegenClient(base_url="http://localhost:8080", timeout=30)

3. **Getting Status:**
   ```bash
   client.poll_status(callback=callback)


