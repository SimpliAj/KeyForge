# tamper_detection.py (unchanged except for clarity)
import os
import hashlib
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def store_checksum(file_path, checksum_file):
    checksum = calculate_checksum(file_path)
    with open(checksum_file, "w") as f:
        f.write(checksum)

def verify_checksum(file_path, checksum_file):
    if not os.path.exists(checksum_file):
        return False
    with open(checksum_file, "r") as f:
        stored_checksum = f.read().strip()
    current_checksum = calculate_checksum(file_path)
    return current_checksum == stored_checksum

def secure_delete(file_path):
    try:
        with open(file_path, "wb") as file:
            file.write(os.urandom(os.path.getsize(file_path)))
        os.remove(file_path)
    except Exception as e:
        print(f"Error securely deleting file: {e}")

def handle_tampering(root):
    files_to_delete = ["encryption_key.key", "master_password.txt", "master_password_checksum.txt", "passwords.json", "notes.json"]
    for file in files_to_delete:
        if os.path.exists(file):
            secure_delete(file)
    messagebox.showerror("Error", "Tampering detected! All data has been deleted.")
    root.quit()

def check_for_tampering(root):
    if os.path.exists("master_password.txt"):
        if not verify_checksum("master_password.txt", "master_password_checksum.txt"):
            handle_tampering(root)
    elif os.path.exists("master_password_checksum.txt") or os.path.exists("passwords.json") or os.path.exists("notes.json"):
        handle_tampering(root)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, root):
        self.root = root
    
    def on_modified(self, event):
        if event.src_path in ["master_password.txt", "passwords.json", "notes.json"]:
            handle_tampering(self.root)

def start_file_monitoring(root):
    observer = Observer()
    observer.schedule(FileChangeHandler(root), path=".", recursive=False)
    observer.start()
    return observer