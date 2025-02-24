import os
import json
import base64
import hashlib
import platform
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pathlib import Path
import sys

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
        pass

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path.cwd()

def is_portable_data_present():
    base_path = get_base_path()
    return os.path.exists(base_path / ".master_password.txt")

def derive_key(master_password, salt=None):
    """Derive an AES key from the master password using PBKDF2."""
    if salt is None:
        salt = os.urandom(16)  # Generate a random salt if not provided
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key for AES
        salt=salt,
        iterations=100000,  # Adjustable for security vs. speed
    )
    key = kdf.derive(master_password.encode())
    return key, salt

def encrypt_data(data, master_password):
    """Encrypt data using AES-GCM with a key derived from the master password."""
    key, salt = derive_key(master_password)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce for AES-GCM
    plaintext = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    encrypted_blob = salt + nonce + ciphertext  # Combine salt, nonce, ciphertext
    return encrypted_blob

def decrypt_data(encrypted_data, master_password):
    """Decrypt data using AES-GCM with a key derived from the master password."""
    salt = encrypted_data[:16]  # First 16 bytes = salt
    nonce = encrypted_data[16:28]  # Next 12 bytes = nonce
    ciphertext = encrypted_data[28:]  # Rest = ciphertext
    key, _ = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode())

def load_passwords(master_password):
    base_path = get_base_path()
    password_file = base_path / ".passwords.json"
    if is_portable_data_present() and os.path.exists(password_file):
        with open(password_file, "rb") as file:
            encrypted_data = file.read()
        try:
            return decrypt_data(encrypted_data, master_password)
        except Exception as e:
            print(f"Error decrypting passwords: {e}")
            return {}
    return {}

def save_passwords(passwords, master_password):
    base_path = get_base_path()
    password_file = base_path / ".passwords.json"
    encrypted_data = encrypt_data(passwords, master_password)
    with open(password_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(password_file)

def load_notes(master_password):
    base_path = get_base_path()
    notes_file = base_path / ".notes.json"
    if is_portable_data_present() and os.path.exists(notes_file):
        with open(notes_file, "rb") as file:
            encrypted_data = file.read()
        try:
            return decrypt_data(encrypted_data, master_password)
        except Exception as e:
            print(f"Error decrypting notes: {e}")
            return {}
    return {}

def save_notes(notes, master_password):
    base_path = get_base_path()
    notes_file = base_path / ".notes.json"
    encrypted_data = encrypt_data(notes, master_password)
    with open(notes_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(notes_file)

def export_password(password_data, passphrase):
    base_path = get_base_path()
    export_file = base_path / ".shared_password.enc"
    encrypted_data = encrypt_data(password_data, passphrase)
    with open(export_file, "wb") as file:
        file.write(encrypted_data)
    set_hidden_attribute(export_file)
    return export_file

def import_password(file_path, passphrase, master_password):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    imported_data = decrypt_data(encrypted_data, passphrase)
    passwords = load_passwords(master_password)
    passwords.update(imported_data)
    save_passwords(passwords, master_password)

def backup_data(master_password):
    files = [".passwords.json", ".notes.json", ".master_password.txt"]
    backup_data = {}
    base_path = get_base_path()
    for file in files:
        file_path = base_path / file
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                backup_data[file] = f.read().hex()
    encrypted_backup = encrypt_data(backup_data, master_password)
    backup_file = base_path / ".backup.enc"
    with open(backup_file, "wb") as file:
        file.write(encrypted_backup)
    set_hidden_attribute(backup_file)
    return backup_file

def restore_data(master_password, backup_file):
    with open(backup_file, "rb") as f:
        encrypted_backup = f.read()
    decrypted_backup = decrypt_data(encrypted_backup, master_password)
    backup_data = json.loads(decrypted_backup)
    base_path = get_base_path()
    for file, content in backup_data.items():
        file_path = base_path / file
        with open(file_path, "wb") as f:
            f.write(bytes.fromhex(content))
        set_hidden_attribute(file_path)
