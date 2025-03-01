# KeyForge

**KeyForge** is a secure, portable password manager built with Python and Tkinter. Protect your credentials and notes with robust encryption, generate strong passwords, and manage everything from a USB stick—across macOS, Windows, and Linux. Featuring a dynamic UI and tamper-proof design, KeyForge keeps your data safe and accessible wherever you go.

<p align="center">
  <img src="https://i.imgur.com/rWUAMW3.png" alt="KeyForge Logo" width="250"/>
</p>

---

## ✨ Features

- **Master Password Protection**: Secure access with a hashed master password; locks out after 3 failed attempts (5-second cooldown) or tampering detection.
- **Encrypted Password Manager**: Store, edit, delete, and copy website credentials. Double-click to reveal passwords (auto-hides after 10s); supports optional 2FA codes.
- **Password Generator**: Create passwords (4-32 characters) with customizable options: lowercase, uppercase, digits, symbols, exclude similar characters, or use Apple-style formatting (18 characters, hyphenated).
- **Secure Notes Manager**: Write, edit, and delete encrypted notes with titles and basic formatting (bold, italic, underline).
- **Tamper Detection**: Monitors critical files (e.g., `.master_password.txt`) and securely wipes data if unauthorized changes are detected.
- **USB Portability**: Runs from a USB stick, storing encrypted, hidden files (e.g., `.passwords.json`, `.notes.json`) alongside the executable.
- **Advanced Tools**:
  - **Password Strength Meter**: Real-time analysis for manually entered passwords.
  - **Expiration Alerts**: Flags passwords older than 90 days with a ⚠️ symbol.
  - **2FA Integration**: Generates TOTP codes for stored accounts.
  - **Secure Sharing**: Export/import passwords with passphrase encryption.
  - **Search & Filter**: Quickly find passwords by website or username.
  - **Backup/Restore**: Create and restore encrypted backups using your master password.
  - **Categories/Tags**: Organize passwords and notes with custom tags.
- **Settings**: Reset master password (re-encrypts data), switch languages (English/Spanish), or clear all data.
- **Clipboard Support**: Copy passwords instantly with a 📋 icon.
- **Dynamic UI**: Adapts window sizes automatically (e.g., Login: 400x250, Manager: 700x850).
- **Custom Icons**: Includes `.icns` (macOS) and `.ico` (Windows) for branded executables.

---

## 🚀 Getting Started

### Running KeyForge
1. **Launch**:
   - Use `main.py` (source) or a prebuilt executable (e.g., `KeyForge-macos.app`, `KeyForge.exe`) from a USB stick.
   - Set a master password on first launch.
2. **Login**: Enter your master password to access the app.
3. **Navigate**: Choose from Password Generator, Password Manager, Notes Manager, or Settings.

### Using Key Features
- **Password Manager**: Add credentials, reveal passwords with a double-click, copy with 📋, or search/export/import entries.
- **Password Generator**: Customize length and characters, then copy or apply directly to the manager.
- **Notes Manager**: Create and format notes securely.
- **Settings**: Manage your master password, language, or data backups.

---

## 📋 Requirements

- **Python 3.x** (for source execution)
- **Dependencies** (install with `pip`):
  - `tkinter` ( bundled with Python)
  - `cryptography` (for PBKDF2 and AES-GCM encryption)
  - `watchdog` (for tamper detection)
  - `pyotp` (for 2FA support)
  - `pillow` (for logo rendering)

---

## 🛠️ Installation (Source)

1. Clone or download the repository.
   ```bash
   git clone https://github.com/yourusername/keyforge.git
   ```
2. Install dependencies:
   ```bash
   pip install cryptography watchdog pyotp pillow
   ```
3. Run the script using the following command:
   ```bash
   python main.py
   ```

## 📦 Building Executables
To create standalone executables for USB use with custom icons (macos.icns for macOS, windows.ico for Windows):
- macOS:
  ```bash
  pyinstaller --onefile --windowed --icon=macos.icns --name KeyForge-macos --add-data "rWUAMW3.png:." --hidden-import=tkinter --hidden-import=cryptography --hidden-import=pyotp --hidden-import=watchdog --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk main.py
  ```
- Windows:
  ```bash
  pyinstaller --onefile --noconsole --icon=windows.ico --name KeyForge --add-data "rWUAMW3.png;." --hidden-import=tkinter --hidden-import=cryptography --hidden-import=pyotp --hidden-import=watchdog --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk main.py
  ```
- Linux:
  ```bash
  pyinstaller --onefile --name KeyForge-linux --add-data "rWUAMW3.png:." --hidden-import=tkinter --hidden-import=cryptography --hidden-import=pyotp --hidden-import=watchdog --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk main.py
  ```
Copy now the Executables on to the USB Stick

## 📂 File Structure

- `main.py`: Core logic and GUI orchestration.
- `design_config.py`: Themes, window sizes, language settings.
- `encryption_utils.py`: Encryption, file I/O, backup/restore.
- `tamper_detection.py`: File monitoring and tamper response.
- `password_utils.py`: Password generation and strength analysis.
- `gui.py`: GUI components for all screens.

Hidden and encrypted files: `.master_password.txt`, `.passwords.json`, `.notes.json`.

## 🔒 Security Highlights

- **Encryption:** Uses PBKDF2 to derive a key from the master password, combined with AES-GCM for data confidentiality and integrity.
- **Master Password:** SHA-256 hashed, stored with checksum.
- **Tamper Detection:** `watchdog` monitors critical files; wipes data on unauthorized changes.
- **Hidden Files:** Data files prefixed with . (hidden on macOS/Linux) and marked hidden on Windows.
- **2FA:** Supports TOTP codes for enhanced security.
- **Secure Deletion:** Overwrites files with random data before deletion.

## 📌 To-Do

[] Browser Extension: Integrate with Chrome/Firefox for autofill.
[] UI Upgrade: Modernize Tkinter or port to a web framework.
[] Enhanced Notes: Add rich text formatting (e.g., colors, lists).
[] Auto Updater: Automatic Update for the .exe or macos executable (download via releases)

## ⚠️ BUGS & ISSUES:
✅ Hidden file creation bug on macOS .app builds fixed—files now correctly appear in the same directory as the executable.

## 🔄 Key Updates
- **Encryption**: Changed from "Fernet encryption" to "PBKDF2 and AES-GCM" to reflect the new method.
- **File Structure**: Removed `.encryption_key.key` since it’s no longer used.
- **Security Features**: Updated encryption description to emphasize master password dependency and removed static key references.
- **Settings**: Clarified that resetting the master password re-encrypts data.
- **Themes**: Removed "toggle themes" from Settings since it’s not implemented yet (only dark theme exists).

## 🤝 Contributing

We welcome contributions! To get involved:

1. Fork this repository.
2. Submit pull requests with bug fixes or new features.
3. Report issues or suggest improvements via Issues.

## 📜 License
KeyForge is released under the MIT License. Feel free to use, modify, and distribute it as you see fit!
