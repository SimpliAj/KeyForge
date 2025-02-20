# encryption_utils.py
import os
from cryptography.fernet import Fernet
import json

def generate_or_load_key():
    key_file = "encryption_key.key"
    try:
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            print("Encryption key generated and saved successfully.")
        return key
    except Exception as e:
        print(f"Error generating or loading encryption key: {e}")
        return None

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def load_passwords(key):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    return {}

def save_passwords(passwords, key):
    data = json.dumps(passwords)
    encrypted_data = encrypt_data(data, key)
    with open("passwords.json", "wb") as file:
        file.write(encrypted_data)

def load_notes(key):
    if os.path.exists("notes.json"):
        with open("notes.json", "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    return {}

def save_notes(notes, key):
    data = json.dumps(notes)
    encrypted_data = encrypt_data(data, key)
    with open("notes.json", "wb") as file:
        file.write(encrypted_data)