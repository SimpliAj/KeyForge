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
        print(f"Setting hidden attribute not implemented for {file_path} on non-Windows")

def get_base_path():
    if getattr(sys, 'frozen', False):
        exe_path = Path(sys.executable)
        # Check if running inside an .app bundle on macOS by looking for Contents/MacOS in the path
        if platform.system() == "Darwin" and "Contents/MacOS" in str(exe_path):
            # Go up to the directory containing the .app bundle
            base_path = exe_path.parents[3]  # /path/to/MyApp.app/Contents/MacOS/ -> /path/to/
        else:
            base_path = exe_path.parent  # For Unix executable: /path/to/
        # Handle PyInstaller temp directory extraction on macOS
        if platform.system() == "Darwin" and '_MEI' in str(base_path):
            base_path = Path(sys.argv[0]).resolve().parent
        print(f"Running as frozen app")
        print(f"Original executable path: {sys.executable}")
        print(f"Resolved base path: {base_path}")
        print(f"Base path exists: {base_path.exists()}")
        print(f"Base path writable: {os.access(base_path, os.W_OK)}")
        return base_path
    base_path = Path.cwd()
    print(f"Running as script")
    print(f"Current working directory: {base_path}")
    print(f"Base path exists: {base_path.exists()}")
    print(f"Base path writable: {os.access(base_path, os.W_OK)}")
    return base_path

def is_portable_data_present():
    base_path = get_base_path()
    master_file = base_path / ".master_password.txt"
    exists = os.path.exists(master_file)
    print(f"Checking portable data at {master_file}: Exists={exists}")
    return exists

def derive_key(master_password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(master_password.encode())
    print(f"Derived encryption key, salt length: {len(salt)}")
    return key, salt

def encrypt_data(data, master_password):
    key, salt = derive_key(master_password)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    plaintext = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    encrypted_blob = salt + nonce + ciphertext
    print(f"Encrypted data, blob size: {len(encrypted_blob)} bytes")
    return encrypted_blob

def decrypt_data(encrypted_data, master_password):
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    ciphertext = encrypted_data[28:]
    key, _ = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    print(f"Decrypted data, plaintext size: {len(plaintext)} bytes")
    return json.loads(plaintext.decode())

def load_passwords(master_password):
    base_path = get_base_path()
    password_file = base_path / ".passwords.json"
    print(f"Attempting to load passwords from: {password_file}")
    if is_portable_data_present() and os.path.exists(password_file):
        with open(password_file, "rb") as file:
            encrypted_data = file.read()
            print(f"Read {len(encrypted_data)} bytes from {password_file}")
        try:
            data = decrypt_data(encrypted_data, master_password)
            print(f"Successfully loaded passwords from {password_file}")
            return data
        except Exception as e:
            print(f"Error decrypting passwords: {e}")
            return {}
    print(f"No passwords file found at {password_file}, returning empty dict")
    return {}

def save_passwords(passwords, master_password):
    base_path = get_base_path()
    password_file = base_path / ".passwords.json"
    print(f"Attempting to save passwords to: {password_file}")
    try:
        encrypted_data = encrypt_data(passwords, master_password)
        print(f"Generated encrypted data for passwords, size: {len(encrypted_data)} bytes")
        with open(password_file, "wb") as file:
            print(f"Opened {password_file} for writing")
            file.write(encrypted_data)
            file.flush()
            os.fsync(file.fileno())
            print(f"Wrote {len(encrypted_data)} bytes to {password_file}")
        set_hidden_attribute(password_file)
        if os.path.exists(password_file):
            print(f"Successfully saved passwords to: {password_file}")
        else:
            print(f"File {password_file} was not created after write")
    except Exception as e:
        print(f"Error saving passwords: {e}")
        raise

def load_notes(master_password):
    base_path = get_base_path()
    notes_file = base_path / ".notes.json"
    print(f"Attempting to load notes from: {notes_file}")
    if is_portable_data_present() and os.path.exists(notes_file):
        with open(notes_file, "rb") as file:
            encrypted_data = file.read()
            print(f"Read {len(encrypted_data)} bytes from {notes_file}")
        try:
            data = decrypt_data(encrypted_data, master_password)
            print(f"Successfully loaded notes from {notes_file}")
            return data
        except Exception as e:
            print(f"Error decrypting notes: {e}")
            return {}
    print(f"No notes file found at {notes_file}, returning empty dict")
    return {}

def save_notes(notes, master_password):
    base_path = get_base_path()
    notes_file = base_path / ".notes.json"
    print(f"Attempting to save notes to: {notes_file}")
    try:
        encrypted_data = encrypt_data(notes, master_password)
        print(f"Generated encrypted data for notes, size: {len(encrypted_data)} bytes")
        with open(notes_file, "wb") as file:
            print(f"Opened {notes_file} for writing")
            file.write(encrypted_data)
            file.flush()
            os.fsync(file.fileno())
            print(f"Wrote {len(encrypted_data)} bytes to {notes_file}")
        set_hidden_attribute(notes_file)
        if os.path.exists(notes_file):
            print(f"Successfully saved notes to: {notes_file}")
        else:
            print(f"File {notes_file} was not created after write")
    except Exception as e:
        print(f"Error saving notes: {e}")
        raise

def export_password(password_data, passphrase):
    base_path = get_base_path()
    export_file = base_path / ".shared_password.enc"
    print(f"Attempting to export password to: {export_file}")
    try:
        encrypted_data = encrypt_data(password_data, passphrase)
        with open(export_file, "wb") as file:
            file.write(encrypted_data)
            file.flush()
            os.fsync(file.fileno())
        set_hidden_attribute(export_file)
        print(f"Exported password to: {export_file}")
        return export_file
    except Exception as e:
        print(f"Error exporting password: {e}")
        raise

def import_password(file_path, passphrase, master_password):
    print(f"Attempting to import password from: {file_path}")
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        imported_data = decrypt_data(encrypted_data, passphrase)
        passwords = load_passwords(master_password)
        passwords.update(imported_data)
        save_passwords(passwords, master_password)
    except Exception as e:
        print(f"Error importing password: {e}")
        raise

def backup_data(master_password):
    files = [".passwords.json", ".notes.json", ".master_password.txt"]
    backup_data = {}
    base_path = get_base_path()
    for file in files:
        file_path = base_path / file
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                backup_data[file] = f.read().hex()
    backup_file = base_path / ".backup.enc"
    print(f"Attempting to create backup at: {backup_file}")
    try:
        encrypted_backup = encrypt_data(backup_data, master_password)
        with open(backup_file, "wb") as file:
            file.write(encrypted_backup)
            file.flush()
            os.fsync(file.fileno())
        set_hidden_attribute(backup_file)
        print(f"Created backup at: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Error creating backup: {e}")
        raise

def restore_data(master_password, backup_file):
    print(f"Attempting to restore from backup: {backup_file}")
    try:
        with open(backup_file, "rb") as file:
            encrypted_backup = file.read()
        decrypted_backup = decrypt_data(encrypted_backup, master_password)
        backup_data = json.loads(decrypted_backup)
        base_path = get_base_path()
        for file, content in backup_data.items():
            file_path = base_path / file
            with open(file_path, "wb") as f:
                f.write(bytes.fromhex(content))
                f.flush()
                os.fsync(f.fileno())
            set_hidden_attribute(file_path)
            print(f"Restored file: {file_path}")
    except Exception as e:
        print(f"Error restoring data: {e}")
        raise
