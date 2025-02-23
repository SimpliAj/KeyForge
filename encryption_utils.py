import os
import json
import base64
import hashlib
import sys
import platform
from pathlib import Path
from cryptography.fernet import Fernet

# For Windows hidden attribute
if platform.system() == "Windows":
    import ctypes
    from ctypes import wintypes

    def set_hidden_attribute(file_path):
        FILE_ATTRIBUTE_HIDDEN = 0x2
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        success = kernel32.SetFileAttributesW(str(file_path), FILE_ATTRIBUTE_HIDDEN)
        if not success:
            print(f"Failed to hide {file_path}: {ctypes.get_last_error()}")
else:
    def set_hidden_attribute(file_path):
        pass  # No-op on non-Windows systems

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path.cwd()

def is_portable_data_present():
    base_path = get_base_path()
    return os.path.exists(base_path / ".encryption_key.key") and os.path.exists(base_path / ".master_password.txt")

def generate_or_load_key():
    base_path = get_base_path()
    key_file = base_path / ".encryption_key.key"
    try:
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            set_hidden_attribute(key_file)
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
    base_path = get_base_path()
    password_file = base_path / ".passwords.json"
    if is_portable_data_present() and os.path.exists(password_file):
        with open(password_file, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    return {}

def save_passwords(passwords, key):
    import time
    for website in passwords:
        if "last_updated" not in passwords[website]:
            passwords[website]["last_updated"] = time.time()
    data = json.dumps(passwords)
    encrypted_data = encrypt_data(data, key)
    password_file = get_base_path() / ".passwords.json"
    with open(password_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(password_file)

def load_notes(key):
    base_path = get_base_path()
    notes_file = base_path / ".notes.json"
    if is_portable_data_present() and os.path.exists(notes_file):
        with open(notes_file, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    return {}

def save_notes(notes, key):
    data = json.dumps(notes)
    encrypted_data = encrypt_data(data, key)
    notes_file = get_base_path() / ".notes.json"
    with open(notes_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(notes_file)

def export_password(password_data, passphrase):
    key = hashlib.sha256(passphrase.encode()).digest()[:32]
    fernet = Fernet(base64.urlsafe_b64encode(key))
    encrypted_data = fernet.encrypt(json.dumps(password_data).encode())
    export_file = get_base_path() / ".shared_password.enc"
    with open(export_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(export_file)
    return export_file

def import_password(file_path, passphrase, key):
    key_derived = hashlib.sha256(passphrase.encode()).digest()[:32]
    fernet = Fernet(base64.urlsafe_b64encode(key_derived))
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    passwords = load_passwords(key)
    passwords.update(json.loads(decrypted_data))
    save_passwords(passwords, key)

def backup_data(key):
    files = [".passwords.json", ".notes.json", ".master_password.txt"]
    backup_data = {}
    base_path = get_base_path()
    for file in files:
        file_path = base_path / file
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                backup_data[file] = f.read().hex()
    encrypted_backup = encrypt_data(json.dumps(backup_data), key)
    backup_file = base_path / ".backup.enc"
    with open(backup_file, "wb") as file:
        file.write(encrypted_backup)
    set_hidden_attribute(backup_file)
    return backup_file

def restore_data(key, backup_file):
    with open(backup_file, "rb") as f:
        encrypted_backup = f.read()
    decrypted_backup = decrypt_data(encrypted_backup, key)
    backup_data = json.loads(decrypted_backup)
    base_path = get_base_path()
    for file, content in backup_data.items():
        file_path = base_path / file
        with open(file_path, "wb") as f:
            f.write(bytes.fromhex(content))
        set_hidden_attribute(file_path)
