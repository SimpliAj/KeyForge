# src/tamper_detection.py
import os
import hashlib
import time
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .encryption_utils import get_base_path, set_hidden_attribute
import design_config

class TamperDetection:
    def __init__(self):
        self.suppress_tampering = False
        self.last_event_time = 0

    def __enter__(self):
        if design_config.DEBUG:
            print("Suppressing tamper detection.")
        self.suppress_tampering = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(0.5)
        if design_config.DEBUG:
            print("Resuming tamper detection.")
        self.suppress_tampering = False

    def calculate_checksum(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def store_checksum(self, file_path, checksum_file):
        checksum = self.calculate_checksum(file_path)
        try:
            with open(checksum_file, "w") as f:
                f.write(checksum)
            set_hidden_attribute(checksum_file)
            if design_config.DEBUG:
                print(f"Stored checksum for {file_path} at {checksum_file}: {checksum}")
        except Exception as e:
            if design_config.DEBUG:
                print(f"Error storing checksum: {e}")

    def verify_checksum(self, file_path, checksum_file):
        if not os.path.exists(checksum_file):
            if design_config.DEBUG:
                print(f"Checksum file {checksum_file} does not exist.")
            return False
        with open(checksum_file, "r") as f:
            stored_checksum = f.read().strip()
        current_checksum = self.calculate_checksum(file_path)
        result = current_checksum == stored_checksum
        if design_config.DEBUG:
            print(f"Verifying {file_path}: stored={stored_checksum}, current={current_checksum}, match={result}")
        return result

    def secure_delete(self, file_path):
        try:
            with open(file_path, "wb") as file:
                file.write(os.urandom(os.path.getsize(file_path)))
            os.remove(file_path)
            if design_config.DEBUG:
                print(f"Securely deleted {file_path}")
        except Exception as e:
            if design_config.DEBUG:
                print(f"Error securely deleting file: {e}")

    def handle_tampering(self, root):
        base_path = get_base_path()
        files_to_delete = [
            base_path / ".master_password.txt",
            base_path / ".master_password_checksum.txt",
            base_path / ".passwords.json",
            base_path / ".notes.json"
        ]
        for file in files_to_delete:
            if os.path.exists(file):
                self.secure_delete(file)
        messagebox.showerror("Error", "Tampering detected! All data has been deleted.")
        root.quit()

    def check_for_tampering(self, root):
        base_path = get_base_path()
        master_password_file = base_path / ".master_password.txt"
        checksum_file = base_path / ".master_password_checksum.txt"
        if os.path.exists(master_password_file):
            if not self.verify_checksum(master_password_file, checksum_file):
                if design_config.DEBUG:
                    print("Checksum mismatch detected.")
                self.handle_tampering(root)
        elif os.path.exists(checksum_file) or os.path.exists(base_path / ".passwords.json") or os.path.exists(base_path / ".notes.json"):
            if design_config.DEBUG:
                print("Inconsistent data files detected.")
            self.handle_tampering(root)
        else:
            if design_config.DEBUG:
                print("No tampering detected.")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, root, tamper_detector):
        self.root = root
        self.tamper_detector = tamper_detector
    
    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.tamper_detector.last_event_time < 0.2:
            if design_config.DEBUG:
                print(f"Debounced event: {event.src_path}")
            return
        self.tamper_detector.last_event_time = current_time
        
        if self.tamper_detector.suppress_tampering:
            if design_config.DEBUG:
                print(f"Ignoring file change during app operation: {event.src_path}")
            return
        base_path = get_base_path()
        monitored_files = [base_path / ".master_password.txt", base_path / ".passwords.json", base_path / ".notes.json"]
        if event.src_path in [str(f) for f in monitored_files]:
            if design_config.DEBUG:
                print(f"Tampering detected via file change: {event.src_path}")
            self.tamper_detector.handle_tampering(self.root)
        else:
            if design_config.DEBUG:
                print(f"Non-monitored file changed: {event.src_path}")

def start_file_monitoring(root, tamper_detector):
    observer = Observer()
    observer.schedule(FileChangeHandler(root, tamper_detector), path=str(get_base_path()), recursive=False)
    observer.start()
    if design_config.DEBUG:
        print(f"Started file monitoring at {get_base_path()}")
    return observer