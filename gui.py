# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from design_config import *

def create_login_screen(root, login_callback, language="en"):
    login_screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(login_screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(login_screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    tk.Label(login_screen, text=LANGUAGES[language]["master_password"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    master_password_entry = ttk.Entry(login_screen, width=30, font=FONT_SMALL, show="*")
    master_password_entry.pack(pady=5)
    ttk.Button(login_screen, text=LANGUAGES[language]["login"], command=lambda: login_callback(master_password_entry)).pack(pady=10)
    return login_screen, master_password_entry

def create_menu_screen(root, generator_callback, manager_callback, notes_callback, settings_callback, logout_callback, language="en"):
    menu_screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(menu_screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(menu_screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    ttk.Button(menu_screen, text=LANGUAGES[language]["password_generator"], command=generator_callback).pack(pady=10)
    ttk.Button(menu_screen, text=LANGUAGES[language]["password_manager"], command=manager_callback).pack(pady=10)
    ttk.Button(menu_screen, text=LANGUAGES[language]["notes_manager"], command=notes_callback).pack(pady=10)
    ttk.Button(menu_screen, text=LANGUAGES[language]["settings"], command=settings_callback).pack(pady=10)
    ttk.Button(menu_screen, text=LANGUAGES[language]["logout"], command=logout_callback).pack(pady=10)
    return menu_screen

def create_password_generator_screen(root, back_callback, generate_callback, language="en"):
    screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    length_label = tk.Label(screen, text="Password Length: 12", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    length_label.pack(pady=5)
    length_slider = ttk.Scale(screen, from_=4, to=32, orient=tk.HORIZONTAL, length=300)
    length_slider.set(12)
    length_slider.pack(pady=5)
    vars_dict = {
        'lowercase': tk.BooleanVar(value=True),
        'uppercase': tk.BooleanVar(value=True),
        'digits': tk.BooleanVar(value=True),
        'symbols': tk.BooleanVar(value=True),
        'exclude': tk.BooleanVar(value=False),
        'apple': tk.BooleanVar(value=False),
        'strength': tk.BooleanVar(value=False)
    }
    tk.Checkbutton(screen, text="Include Lowercase Letters", variable=vars_dict['lowercase'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Uppercase Letters", variable=vars_dict['uppercase'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Digits", variable=vars_dict['digits'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Symbols", variable=vars_dict['symbols'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Exclude Similar Characters (e.g., i, l, 1, L, o, 0, O)", variable=vars_dict['exclude'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL).pack(pady=2)
    
    # Updated Apple Formatting checkbox with inline state management
    tk.Checkbutton(screen, text="Apple Formatting (18 characters, no symbols)", variable=vars_dict['apple'], 
                   bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], 
                   font=FONT_SMALL, 
                   command=lambda: [length_slider.config(state="disabled" if vars_dict['apple'].get() else "normal"), 
                                   length_slider.set(18) if vars_dict['apple'].get() else None, 
                                   length_label.config(text=f"Password Length: {18 if vars_dict['apple'].get() else int(length_slider.get())}")]).pack(pady=2)
    
    strength_check = tk.Checkbutton(screen, text="Show Password Strength Meter", variable=vars_dict['strength'], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], selectcolor=DARK_THEME["SELECT_COLOR"], font=FONT_SMALL)
    strength_check.pack(pady=2)
    strength_meter = ttk.Progressbar(screen, orient=tk.HORIZONTAL, length=300, mode="determinate", maximum=100)
    strength_meter.pack(pady=10)
    ttk.Button(screen, text="Generate Password", command=lambda: generate_callback(length_slider, vars_dict, password_entry, strength_meter, length_label)).pack(pady=10)
    password_entry = ttk.Entry(screen, width=30, font=FONT_SMALL)
    password_entry.pack(pady=5)
    ttk.Button(screen, text="Copy to Clipboard", command=lambda: root.clipboard_append(password_entry.get())).pack(pady=5)
    ttk.Button(screen, text=LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    return screen, length_slider, vars_dict, password_entry, strength_meter, length_label

def create_password_manager_screen(root, back_callback, add_callback, delete_callback, generate_callback, language="en"):
    screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    tk.Label(screen, text="Website:", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    website_entry = ttk.Entry(screen, width=30, font=FONT_SMALL)
    website_entry.pack(pady=5)
    tk.Label(screen, text="Username:", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    username_entry = ttk.Entry(screen, width=30, font=FONT_SMALL)
    username_entry.pack(pady=5)
    tk.Label(screen, text="Password:", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    password_frame = tk.Frame(screen, bg=DARK_THEME["BG_COLOR"])
    password_frame.pack(pady=5)
    password_entry = ttk.Entry(password_frame, width=30, font=FONT_SMALL)
    password_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(password_frame, text="🔑", width=3, command=generate_callback).pack(side=tk.LEFT)
    ttk.Button(screen, text="Add Password", command=lambda: add_callback(website_entry, username_entry, password_entry)).pack(pady=10)
    password_tree = ttk.Treeview(screen, columns=("Website", "Username", "Password", "Copy"), show="headings", height=10)
    password_tree.heading("Website", text="Website")
    password_tree.heading("Username", text="Username")
    password_tree.heading("Password", text="Password")
    password_tree.heading("Copy", text="Copy")
    password_tree.column("Website", width=200)
    password_tree.column("Username", width=150)
    password_tree.column("Password", width=150)
    password_tree.column("Copy", width=50)
    password_tree.pack(pady=10)
    ttk.Button(screen, text="Delete Password", command=lambda: delete_callback(password_tree)).pack(pady=10)
    ttk.Button(screen, text=LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    return screen, website_entry, username_entry, password_entry, password_tree

def create_notes_manager_screen(root, back_callback, add_callback, edit_callback, delete_callback, language="en"):
    screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    main_frame = tk.Frame(screen, bg=DARK_THEME["BG_COLOR"])
    main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    notes_tree = ttk.Treeview(main_frame, columns=("Title",), show="headings", height=15)
    notes_tree.heading("Title", text="Notes")
    notes_tree.column("Title", width=200)
    notes_tree.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    editor_frame = tk.Frame(main_frame, bg=DARK_THEME["BG_COLOR"])
    editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
    tk.Label(editor_frame, text=LANGUAGES[language]["note_title"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    title_entry = ttk.Entry(editor_frame, width=40, font=FONT_SMALL)
    title_entry.pack(pady=5)
    text_editor = tk.Text(editor_frame, height=15, width=50, font=FONT_SMALL, bg=DARK_THEME["SELECT_COLOR"], fg=DARK_THEME["FG_COLOR"], insertbackground=DARK_THEME["FG_COLOR"])
    text_editor.pack(pady=5)
    format_frame = tk.Frame(editor_frame, bg=DARK_THEME["BG_COLOR"])
    format_frame.pack(pady=5)
    ttk.Button(format_frame, text="B", width=3, command=lambda: text_editor.tag_add("bold", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    ttk.Button(format_frame, text="I", width=3, command=lambda: text_editor.tag_add("italic", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    ttk.Button(format_frame, text="U", width=3, command=lambda: text_editor.tag_add("underline", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    text_editor.tag_configure("bold", font=(FONT[0], FONT[1], "bold"))
    text_editor.tag_configure("italic", font=(FONT[0], FONT[1], "italic"))
    text_editor.tag_configure("underline", underline=True)
    action_frame = tk.Frame(screen, bg=DARK_THEME["BG_COLOR"])
    action_frame.pack(pady=10)
    ttk.Button(action_frame, text=LANGUAGES[language]["add_note"], command=lambda: add_callback(title_entry, text_editor)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=LANGUAGES[language]["edit_note"], command=lambda: edit_callback(notes_tree, title_entry, text_editor)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=LANGUAGES[language]["delete_note"], command=lambda: delete_callback(notes_tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=LANGUAGES[language]["back_to_menu"], command=back_callback).pack(side=tk.LEFT, padx=5)
    return screen, notes_tree, title_entry, text_editor

def create_settings_screen(root, back_callback, reset_password_callback, update_language_callback, clear_data_callback, language="en"):
    screen = tk.Frame(root, bg=DARK_THEME["BG_COLOR"])
    logo_photo = load_logo()
    logo_label = tk.Label(screen, image=logo_photo, bg=DARK_THEME["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)

    # Reset Master Password
    tk.Label(screen, text=LANGUAGES[language]["reset_master_password"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    tk.Label(screen, text=LANGUAGES[language]["new_master_password"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT_SMALL).pack()
    new_password_entry = ttk.Entry(screen, width=30, font=FONT_SMALL, show="*")
    new_password_entry.pack(pady=2)
    tk.Label(screen, text=LANGUAGES[language]["confirm_master_password"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT_SMALL).pack()
    confirm_password_entry = ttk.Entry(screen, width=30, font=FONT_SMALL, show="*")
    confirm_password_entry.pack(pady=2)
    ttk.Button(screen, text="Reset", command=lambda: reset_password_callback(new_password_entry, confirm_password_entry)).pack(pady=10)

    # Language Selection
    tk.Label(screen, text=LANGUAGES[language]["language"], bg=DARK_THEME["BG_COLOR"], fg=DARK_THEME["FG_COLOR"], font=FONT).pack(pady=5)
    language_var = tk.StringVar(value=language)
    ttk.Combobox(screen, textvariable=language_var, values=["en", "es"], state="readonly").pack(pady=5)
    ttk.Button(screen, text="Apply", command=lambda: update_language_callback(language_var.get())).pack(pady=5)

    # Clear All Data
    ttk.Button(screen, text=LANGUAGES[language]["clear_all_data"], command=clear_data_callback).pack(pady=10)

    # Back to Menu
    ttk.Button(screen, text=LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    
    return screen, new_password_entry, confirm_password_entry

def load_logo():
    try:
        if os.path.exists(LOGO_PATH):
            logo_image = Image.open(LOGO_PATH)
            logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(logo_image)
    except Exception as e:
        print(f"Error loading logo: {e}")
    return None