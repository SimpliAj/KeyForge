# design_config.py
DARK_THEME = {"BG_COLOR": "#2E3440", "FG_COLOR": "#D8DEE9", "SELECT_COLOR": "#3B4252"}
LIGHT_THEME = {"BG_COLOR": "#FFFFFF", "FG_COLOR": "#000000", "SELECT_COLOR": "#D3D3D3"}

FONT = ("Arial", 12)
FONT_SMALL = ("Arial", 10)

LOGIN_WINDOW_SIZE = "400x250"
MENU_WINDOW_SIZE = "400x400"
PASSWORD_GENERATOR_WINDOW_SIZE = "400x550"
PASSWORD_MANAGER_WINDOW_SIZE = "700x850"
NOTES_MANAGER_WINDOW_SIZE = "600x750"
SETTINGS_WINDOW_SIZE = "400x700"
LOGO_PATH = "KeyForge.png"

DEBUG = False  # Set to False to disable debug logs

LANGUAGES = {
    "en": {
        "login": "Login",
        "master_password": "Master Password:",
        "password_generator": "Password Generator",
        "password_manager": "Password Manager",
        "notes_manager": "Notes Manager",
        "settings": "Settings",
        "logout": "Logout",
        "back_to_menu": "Back to Menu",
        "reset_master_password": "Reset Master Password",
        "new_master_password": "New Master Password:",
        "confirm_master_password": "Confirm New Master Password:",
        "language": "Language:",
        "theme": "Theme:",
        "clear_all_data": "Clear All Data",
        "dark": "Dark",
        "light": "Light",
        "add_note": "Add Note",
        "edit_note": "Edit Note",
        "delete_note": "Delete Note",
        "note_title": "Note Title:",
        "search": "Search:",
        "twofa_secret": "2FA Secret (optional):",
        "category_tag": "Category/Tag:",
        "export_password": "Export Password",
        "import_password": "Import Password",
        "backup_data": "Backup Data",
        "restore_data": "Restore Data"
    },
    "es": {
        "login": "Iniciar Sesión",
        "master_password": "Contraseña Maestra:",
        "password_generator": "Generador de Contraseñas",
        "password_manager": "Gestor de Contraseñas",
        "notes_manager": "Gestor de Notas",
        "settings": "Configuraciones",
        "logout": "Cerrar Sesión",
        "back_to_menu": "Volver al Menú",
        "reset_master_password": "Restablecer Contraseña Maestra",
        "new_master_password": "Nueva Contraseña Maestra:",
        "confirm_master_password": "Confirmar Nueva Contraseña Maestra:",
        "language": "Idioma:",
        "theme": "Tema:",
        "clear_all_data": "Borrar Todos los Datos",
        "dark": "Oscuro",
        "light": "Claro",
        "add_note": "Agregar Nota",
        "edit_note": "Editar Nota",
        "delete_note": "Eliminar Nota",
        "note_title": "Título de la Nota:",
        "search": "Buscar:",
        "twofa_secret": "Secreto 2FA (opcional):",
        "category_tag": "Categoría/Etiqueta:",
        "export_password": "Exportar Contraseña",
        "import_password": "Importar Contraseña",
        "backup_data": "Respaldar Datos",
        "restore_data": "Restaurar Datos"
    }
}