import random
import time
import requests
from Crypto.Cipher import ChaCha20
import base64
import secrets

# Function to simulate sensor data
def generate_sensor_data():
    return {
        "temperature": round(random.uniform(35.0, 40.0), 2),
        "activity": random.randint(0, 100)
    }

# Function to encrypt data
def encrypt_data(data, key):
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + ciphertext).decode('utf-8')

# HTTP transmission simulation
def transmit_data(data):
    url = 'http://localhost:5000/receive-data'
    payload = {"data": data}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Data transmitted: {response._content.decode()}")

key = secrets.token_bytes(32)  # Generate a random 256-bit key
  
while True:
    data = generate_sensor_data()
    encrypted_data = encrypt_data(str(data), key)
    transmit_data(encrypted_data)
    time.sleep(300)  # Send data every 5 minutes
