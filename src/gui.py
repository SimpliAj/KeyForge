# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys
from pathlib import Path
import design_config
from .password_utils import analyze_password_strength

def load_logo(base_path):
    try:
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
            if design_config.DEBUG:
                print(f"Running in frozen mode, base_path: {base_path}")
        else:
            if design_config.DEBUG:
                print(f"Using provided base_path: {base_path}")
        
        logo_path = base_path / "images" / design_config.LOGO_PATH
        if design_config.DEBUG:
            print(f"Looking for logo at: {logo_path}")
        
        if logo_path.exists():
            if design_config.DEBUG:
                print(f"Logo file found at: {logo_path}")
            logo_image = Image.open(logo_path)
            if design_config.DEBUG:
                print(f"Image opened successfully, size: {logo_image.size}")
            logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(logo_image)
            if design_config.DEBUG:
                print(f"Image converted to PhotoImage")
            return photo
        else:
            if design_config.DEBUG:
                print(f"Logo file NOT found at: {logo_path}")
                print(f"Current directory contents: {os.listdir(base_path)}")
                if os.path.exists(base_path / "images"):
                    print(f"Images directory contents: {os.listdir(base_path / 'images')}")
                else:
                    print(f"Images directory does not exist at: {base_path / 'images'}")
    except Exception as e:
        if design_config.DEBUG:
            print(f"Error loading logo: {e}")
    return None

def create_login_screen(root, login_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    login_screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(login_screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(login_screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    tk.Label(login_screen, text=design_config.LANGUAGES[language]["master_password"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    master_password_entry = ttk.Entry(login_screen, width=30, font=design_config.FONT_SMALL, show="*")
    master_password_entry.pack(pady=5)
    ttk.Button(login_screen, text=design_config.LANGUAGES[language]["login"], command=lambda: login_callback(master_password_entry)).pack(pady=10)
    return login_screen, master_password_entry

def create_menu_screen(root, generator_callback, manager_callback, notes_callback, settings_callback, logout_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    menu_screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(menu_screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(menu_screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    ttk.Button(menu_screen, text=design_config.LANGUAGES[language]["password_generator"], command=generator_callback).pack(pady=10)
    ttk.Button(menu_screen, text=design_config.LANGUAGES[language]["password_manager"], command=manager_callback).pack(pady=10)
    ttk.Button(menu_screen, text=design_config.LANGUAGES[language]["notes_manager"], command=notes_callback).pack(pady=10)
    ttk.Button(menu_screen, text=design_config.LANGUAGES[language]["settings"], command=settings_callback).pack(pady=10)
    ttk.Button(menu_screen, text=design_config.LANGUAGES[language]["logout"], command=logout_callback).pack(pady=10)
    return menu_screen

def create_password_generator_screen(root, back_callback, generate_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    length_label = tk.Label(screen, text="Password Length: 12", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
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
    tk.Checkbutton(screen, text="Include Lowercase Letters", variable=vars_dict['lowercase'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Uppercase Letters", variable=vars_dict['uppercase'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Digits", variable=vars_dict['digits'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Include Symbols", variable=vars_dict['symbols'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Exclude Similar Characters (e.g., i, l, 1, L, o, 0, O)", variable=vars_dict['exclude'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL).pack(pady=2)
    tk.Checkbutton(screen, text="Apple Formatting (18 characters, no symbols)", variable=vars_dict['apple'], 
                   bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], 
                   font=design_config.FONT_SMALL, 
                   command=lambda: [length_slider.config(state="disabled" if vars_dict['apple'].get() else "normal"), 
                                   length_slider.set(18) if vars_dict['apple'].get() else None, 
                                   length_label.config(text=f"Password Length: {18 if vars_dict['apple'].get() else int(length_slider.get())}")]).pack(pady=2)
    strength_check = tk.Checkbutton(screen, text="Show Password Strength Meter", variable=vars_dict['strength'], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], selectcolor=theme["SELECT_COLOR"], font=design_config.FONT_SMALL)
    strength_check.pack(pady=2)
    strength_meter = ttk.Progressbar(screen, orient=tk.HORIZONTAL, length=300, mode="determinate", maximum=100)
    strength_meter.pack(pady=10)
    ttk.Button(screen, text="Generate Password", command=lambda: generate_callback(length_slider, vars_dict, password_entry, strength_meter, length_label)).pack(pady=10)
    password_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    password_entry.pack(pady=5)
    ttk.Button(screen, text="Copy to Clipboard", command=lambda: root.clipboard_append(password_entry.get())).pack(pady=5)
    ttk.Button(screen, text=design_config.LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    return screen, length_slider, vars_dict, password_entry, strength_meter, length_label

def create_password_manager_screen(root, back_callback, add_callback, delete_callback, generate_callback, export_callback, import_callback, search_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    
    tk.Label(screen, text=design_config.LANGUAGES[language]["search"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    search_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    search_entry.pack(pady=5)
    search_entry.bind("<KeyRelease>", lambda event: search_callback(search_entry.get()))
    
    tk.Label(screen, text="Website:", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    website_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    website_entry.pack(pady=5)
    tk.Label(screen, text="Username:", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    username_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    username_entry.pack(pady=5)
    tk.Label(screen, text="Password:", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    password_frame = tk.Frame(screen, bg=theme["BG_COLOR"])
    password_frame.pack(pady=5)
    password_entry = ttk.Entry(password_frame, width=30, font=design_config.FONT_SMALL)
    password_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(password_frame, text="🔑", width=3, command=generate_callback).pack(side=tk.LEFT)
    strength_label = tk.Label(password_frame, text="Strength: N/A", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT_SMALL)
    strength_label.pack(side=tk.LEFT, padx=5)
    password_entry.bind("<KeyRelease>", lambda event: update_strength_label(password_entry.get(), strength_label))
    
    tk.Label(screen, text=design_config.LANGUAGES[language]["twofa_secret"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    twofa_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    twofa_entry.pack(pady=5)
    tk.Label(screen, text=design_config.LANGUAGES[language]["category_tag"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    tag_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL)
    tag_entry.pack(pady=5)
    
    action_frame = tk.Frame(screen, bg=theme["BG_COLOR"])
    action_frame.pack(pady=10)
    ttk.Button(action_frame, text="Add Password", command=lambda: add_callback(website_entry, username_entry, password_entry, twofa_entry, tag_entry)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["export_password"], command=lambda: export_callback(password_tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["import_password"], command=import_callback).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text="Delete Password", command=lambda: delete_callback(password_tree)).pack(side=tk.LEFT, padx=5)
    
    password_tree = ttk.Treeview(screen, columns=("Website", "Username", "Password", "Tag", "Copy", "2FA", "Expired"), show="headings", height=10)
    password_tree.heading("Website", text="Website")
    password_tree.heading("Username", text="Username")
    password_tree.heading("Password", text="Password")
    password_tree.heading("Tag", text="Tag")
    password_tree.heading("Copy", text="Copy")
    password_tree.heading("2FA", text="2FA Code")
    password_tree.heading("Expired", text="Expired")
    password_tree.column("Website", width=150)
    password_tree.column("Username", width=100)
    password_tree.column("Password", width=100)
    password_tree.column("Tag", width=100)
    password_tree.column("Copy", width=50)
    password_tree.column("2FA", width=100)
    password_tree.column("Expired", width=50)
    password_tree.pack(pady=10)
    
    ttk.Button(screen, text=design_config.LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    
    screen.strength_label = strength_label
    return screen, website_entry, username_entry, password_entry, password_tree, twofa_entry, tag_entry, search_entry

def update_strength_label(password, label):
    strength, _ = analyze_password_strength(password)
    color = "green" if strength >= 80 else "yellow" if strength >= 40 else "red"
    label.config(text=f"Strength: {strength}%", fg=color)

def create_notes_manager_screen(root, back_callback, add_callback, edit_callback, delete_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
    main_frame = tk.Frame(screen, bg=theme["BG_COLOR"])
    main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    notes_tree = ttk.Treeview(main_frame, columns=("Title",), show="headings", height=15)
    notes_tree.heading("Title", text="Notes")
    notes_tree.column("Title", width=200)
    notes_tree.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    editor_frame = tk.Frame(main_frame, bg=theme["BG_COLOR"])
    editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
    tk.Label(editor_frame, text=design_config.LANGUAGES[language]["note_title"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    title_entry = ttk.Entry(editor_frame, width=40, font=design_config.FONT_SMALL)
    title_entry.pack(pady=5)
    text_editor = tk.Text(editor_frame, height=15, width=50, font=design_config.FONT_SMALL, bg=theme["SELECT_COLOR"], fg=theme["FG_COLOR"], insertbackground=theme["FG_COLOR"])
    text_editor.pack(pady=5)
    format_frame = tk.Frame(editor_frame, bg=theme["BG_COLOR"])
    format_frame.pack(pady=5)
    ttk.Button(format_frame, text="B", width=3, command=lambda: text_editor.tag_add("bold", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    ttk.Button(format_frame, text="I", width=3, command=lambda: text_editor.tag_add("italic", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    ttk.Button(format_frame, text="U", width=3, command=lambda: text_editor.tag_add("underline", "sel.first", "sel.last")).pack(side=tk.LEFT, padx=2)
    text_editor.tag_configure("bold", font=(design_config.FONT[0], design_config.FONT[1], "bold"))
    text_editor.tag_configure("italic", font=(design_config.FONT[0], design_config.FONT[1], "italic"))
    text_editor.tag_configure("underline", underline=True)
    action_frame = tk.Frame(screen, bg=theme["BG_COLOR"])
    action_frame.pack(pady=10)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["add_note"], command=lambda: add_callback(title_entry, text_editor)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["edit_note"], command=lambda: edit_callback(notes_tree, title_entry, text_editor)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["delete_note"], command=lambda: delete_callback(notes_tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(action_frame, text=design_config.LANGUAGES[language]["back_to_menu"], command=back_callback).pack(side=tk.LEFT, padx=5)
    return screen, notes_tree, title_entry, text_editor

def create_settings_screen(root, back_callback, reset_password_callback, update_language_callback, clear_data_callback, backup_callback, restore_callback, update_theme_callback, language="en", theme=design_config.DARK_THEME, base_path=None):
    screen = tk.Frame(root, bg=theme["BG_COLOR"])
    logo_photo = load_logo(base_path)
    logo_label = tk.Label(screen, image=logo_photo, bg=theme["BG_COLOR"]) if logo_photo else tk.Label(screen, text="Logo", bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)

    tk.Label(screen, text=design_config.LANGUAGES[language]["reset_master_password"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    tk.Label(screen, text=design_config.LANGUAGES[language]["new_master_password"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT_SMALL).pack()
    new_password_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL, show="*")
    new_password_entry.pack(pady=2)
    tk.Label(screen, text=design_config.LANGUAGES[language]["confirm_master_password"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT_SMALL).pack()
    confirm_password_entry = ttk.Entry(screen, width=30, font=design_config.FONT_SMALL, show="*")
    confirm_password_entry.pack(pady=2)
    ttk.Button(screen, text="Reset", command=lambda: reset_password_callback(new_password_entry, confirm_password_entry)).pack(pady=10)

    tk.Label(screen, text=design_config.LANGUAGES[language]["language"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    language_var = tk.StringVar(value=language)
    ttk.Combobox(screen, textvariable=language_var, values=["en", "es"], state="readonly").pack(pady=5)
    ttk.Button(screen, text="Apply", command=lambda: update_language_callback(language_var.get())).pack(pady=5)

    tk.Label(screen, text=design_config.LANGUAGES[language]["theme"], bg=theme["BG_COLOR"], fg=theme["FG_COLOR"], font=design_config.FONT).pack(pady=5)
    theme_var = tk.StringVar(value="dark")
    ttk.Combobox(screen, textvariable=theme_var, values=["dark", "light"], state="readonly").pack(pady=5)
    ttk.Button(screen, text="Apply", command=lambda: update_theme_callback(theme_var.get())).pack(pady=5)

    ttk.Button(screen, text=design_config.LANGUAGES[language]["backup_data"], command=backup_callback).pack(pady=5)
    ttk.Button(screen, text=design_config.LANGUAGES[language]["restore_data"], command=restore_callback).pack(pady=5)

    ttk.Button(screen, text=design_config.LANGUAGES[language]["clear_all_data"], command=clear_data_callback).pack(pady=10)

    ttk.Button(screen, text=design_config.LANGUAGES[language]["back_to_menu"], command=back_callback).pack(pady=10)
    
    return screen, new_password_entry, confirm_password_entry