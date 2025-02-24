# KeyForge

KeyForge is a secure, portable password manager built with Python and Tkinter. It provides encrypted password storage, a customizable password generator, a secure notes manager, and settings—all protected by a master password with tamper detection. Designed to run from a USB stick, it’s ideal for managing credentials across macOS, Windows, and Linux with a dynamic, resizable UI.

<p align="center">
  <img src="https://i.imgur.com/rWUAMW3.png" alt="KeyForge Logo" width="250"/>
</p>

## Features

- **Master Password Security**: Access requires a hashed master password; locks out after 3 failed attempts or tampering (5-second cooldown).
- **Encrypted Password Manager**: Store, edit, delete, and copy website credentials with double-click reveal (hides after 10s) and optional 2FA code generation.
- **Password Generator**: Generate passwords (4-32 characters) with options for lowercase, uppercase, digits, symbols, exclusion of similar characters, and Apple-style formatting (18 characters, hyphenated).
- **Secure Notes Manager**: Create, edit, and delete encrypted notes with titles and basic formatting (bold, italic, underline).
- **Tamper Detection**: Monitors critical files (e.g., `.master_password.txt`) for unauthorized changes, securely wiping data if tampering is detected.
- **USB Portability**: Runs from a USB stick, storing all data (e.g., `.passwords.json`, `.notes.json`) as hidden files next to the executable.
- **Extended Features**:
  - **Password Strength Analysis**: Displays strength for manually entered passwords.
  - **Expiration Reminders**: Flags passwords older than 90 days.
  - **2FA Support**: Generates TOTP codes for stored accounts.
  - **Secure Sharing**: Export/import passwords with passphrase encryption.
  - **Search & Filter**: Search passwords by website or username.
  - **Backup/Restore**: Encrypted backups of all data using the master password.
  - **Categories/Tags**: Organize passwords and notes with tags.
- **Settings**: Reset master password (re-encrypts data), switch languages (English/Spanish), or clear all data.
- **Clipboard Integration**: Copy passwords with a clipboard icon.
- **Dynamic UI**: Resizes automatically (login: 400x250, menu: 400x400, generator: 400x625, manager/notes: 600x750, settings: 400x600).
- **Custom Icons**: macOS and Windows builds support `.icns` and `.ico` icons.

## How to Use

1. **Launch KeyForge**:
   - Run `main.py` (source) or the platform-specific executable from a USB stick (e.g., `KeyForge-macos.app`, `KeyForge.exe`).
   - Set a master password on first use.
2. **Login**: Enter your master password.
3. **Main Menu**: Navigate to Password Generator, Password Manager, Notes Manager, or Settings.
4. **Password Manager**:
   - Add credentials (website, username, password, optional 2FA secret, tag).
   - Double-click to reveal passwords; click 📋 to copy.
   - Search/filter entries; export/import with a passphrase.
5. **Password Generator**:
   - Adjust length and character options; toggle strength meter.
   - Copy or use directly in the manager.
6. **Notes Manager**:
   - Add/edit notes with titles and formatting; delete as needed.
7. **Settings**:
   - Reset master password, change language, backup/restore data, or wipe everything.

## Requirements

- **Python 3.x** (for source execution)
- **Libraries** (install via `pip`):
  - `tkinter` (included with Python)
  - `cryptography` (PBKDF2 and AES-GCM encryption)
  - `watchdog` (tamper detection)
  - `pyotp` (2FA support)
  - `pillow` (image handling)

## Installation (Source)

1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install cryptography watchdog pyotp pillow
   ```
3. Run the script using the following command:
   ```bash
   python main.py
   ```

## Building Executables
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

## File Structure

- `main.py`: Core logic and GUI orchestration.
- `design_config.py`: Themes, window sizes, language settings.
- `encryption_utils.py`: Encryption, file I/O, backup/restore.
- `tamper_detection.py`: File monitoring and tamper response.
- `password_utils.py`: Password generation and strength analysis.
- `gui.py`: GUI components for all screens.

Hidden and encrypted files (on USB): `.master_password.txt`, `.passwords.json`, `.notes.json`.

## Security Features

- **Encryption:** Uses PBKDF2 to derive a key from the master password, combined with AES-GCM for data confidentiality and integrity.
- **Master Password:** SHA-256 hashed, stored with checksum.
- **Tamper Detection:** `watchdog` monitors critical files; wipes data on unauthorized changes.
- **Hidden Files:** Data files prefixed with . (hidden on macOS/Linux) and marked hidden on Windows.
- **2FA:** Supports TOTP codes for enhanced security.
- **Secure Deletion:** Overwrites files with random data before deletion.

## To-Do

1. Browser Extension: Integrate with Chrome/Firefox for autofill.
2. UI Upgrade: Modernize Tkinter or port to a web framework.
3. Enhanced Notes: Add rich text formatting (e.g., colors, lists).

### Key Updates
- **Encryption**: Changed from "Fernet encryption" to "PBKDF2 and AES-GCM" to reflect the new method.
- **File Structure**: Removed `.encryption_key.key` since it’s no longer used.
- **Security Features**: Updated encryption description to emphasize master password dependency and removed static key references.
- **Settings**: Clarified that resetting the master password re-encrypts data.
- **Themes**: Removed "toggle themes" from Settings since it’s not implemented yet (only dark theme exists).

## Contributing

Contributions are welcome!
- Submit pull requests for fixes or features.
- Report bugs, suggest enhancements, or raise security issues via GitHub Issues.
