from flask import Flask, request
from Crypto.Cipher import AES
import base64
import requests
import secrets

app = Flask(__name__)
key = secrets.token_bytes(32)

@app.route('/', methods=['GET'])
def hello():
    print(key)
    return 'Hello, World!'

def decrypt_data(encrypted_data):
    raw_data = base64.b64decode(encrypted_data)
    nonce = raw_data[:16]
    ciphertext = raw_data[16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + ciphertext).decode('utf-8')

@app.route('/receive-data', methods=['POST'])
def receive_data():
    encrypted_data = request.json.get('data')
    decrypted_data = decrypt_data(encrypted_data)
    re_encrypted_data = encrypt_data(decrypted_data)
    # Forward the re-encrypted data to the exploitation layer
    url = 'http://localhost:8000/api/sensor-data/'
    payload = {"data": re_encrypted_data}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    return {"status": response.status_code}

if __name__ == '__main__':
    app.run(port=5000)
