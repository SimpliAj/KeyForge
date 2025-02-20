# KeyForge

KeyForge is a secure password manager application built with Python and Tkinter. It offers encrypted password storage, a customizable password generator, a secure notes manager, and settings, all protected by a master password with tamper detection and a dynamic, resizeable UI.

<p align="center">
  <img src="https://i.imgur.com/rWUAMW3.png" alt="KeyForge Logo" width="250"/>
</p>

## Features

- **Master Password Security**: Access requires a hashed master password; locks out after 3 failed attempts or tampering.
- **Encrypted Password Manager**: Store, edit, delete, and copy website credentials securely with double-click reveal (hides after 10s).
- **Password Generator**: Generate passwords (4-32 characters) with options for lowercase, uppercase, digits, symbols, exclusion of similar characters, and Apple-style formatting (18 characters, hyphenated).
- **Secure Notes Manager**: Create, edit, and delete encrypted notes with titles and basic formatting support (bold, italic, underline).
- **Tamper Detection**: Monitors `master_password.txt` for unauthorized changes, resetting data if tampering is detected.
- **Settings**: Reset master password, switch languages, or clear all data.
- **Clipboard Integration**: Copy passwords directly from the manager with a clipboard icon.
- **Password Strength Meter**: Visual feedback on generated password strength (toggleable).
- **Dynamic UI**: Screens resize automatically (login: 400x300, menu: 400x500, manager/generator/notes/settings: 600x500).

## How to Use

1. **Launch KeyForge**: Run `main.py` and set a master password on first use.
2. **Login**: Enter your master password (5-second cooldown between failed attempts).
3. **Main Menu**: Choose Password Generator, Password Manager, Notes Manager, or Settings.
4. **Password Manager**:
   - Add credentials (website, username, password).
   - Double-click to reveal passwords (hides after 10s).
   - Click the clipboard icon to copy passwords.
5. **Password Generator**:
   - Set length (slider) and check character types.
   - Enable "Apple Formatting" for 18-character hyphenated passwords (disables slider).
   - Toggle strength meter and copy generated passwords.
6. **Notes Manager**:
   - Add/edit notes with titles and content.
   - Select notes from the list to load and modify.
7. **Settings**:
   - Reset master password, change language, or wipe all data (with confirmation).

## Requirements

- Python 3.x
- Tkinter (included with Python)
- Additional libraries:
  - `cryptography` (for encryption/decryption)
  - `watchdog` (for tamper detection via file monitoring)

## Installation

1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install cryptography watchdog
   ```
3. Run the script using the following command:
   ```bash
   python KeyForce.py
   ```

## File Structure

- `main.py`: Main application logic and GUI orchestration.
- `design_config.py`: Theme settings (e.g., dark theme) and window sizes.
- `encryption_utils.py`: Encryption key generation, password hashing, and data encryption/decryption.
- `tamper_detection.py`: File monitoring and tamper response logic.
- `password_utils.py`: Password generation and strength calculation.
- `gui.py`: GUI component creation for all screens.

## Security Features

- **Encryption**: Passwords and notes encrypted with a key from `generate_or_load_key()`.
- **Master Password**: Hashed and stored in `master_password.txt` with checksum verification.
- **Tamper Detection**: Uses `watchdog` to monitor `master_password.txt`; triggers reset on tampering.
- **Lockout**: Limits login attempts to 3, with a 5-second cooldown between tries.

## To-Do

1. **Browser Integration**: Add a Chrome extension for password autofill.
2. **UI Modernization**: Enhance Tkinter UI or migrate to a web-based framework.
3. **Advanced Features**:
  - Two-factor authentication support.
  - Richer notes formatting (e.g., colors, bullet lists).

## Contributing

Contributions are welcome! Please:
- Submit pull requests for bug fixes or enhancements.
- Open issues for bugs, feature requests, or security concerns.
