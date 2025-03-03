# main.py
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import time
import pyotp
import design_config
from src.encryption_utils import *
from src.tamper_detection import TamperDetection, start_file_monitoring
from src.password_utils import *
from src.gui import *
import os
from pathlib import Path

class KeyForgeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyForge")
        self.root.geometry(design_config.LOGIN_WINDOW_SIZE)
        self.root.resizable(False, False)
        
        self.master_password = None
        self.tamper_detector = TamperDetection()
        self.failed_attempts = 0
        self.last_attempt_time = 0
        self.current_language = "en"
        
        # Set base_path to the directory containing main.py
        self.base_path = Path(__file__).parent  # project_root/
        if design_config.DEBUG:
            print(f"Initialized base_path: {self.base_path}")
        
        self.load_theme()
        self.root.configure(bg=self.current_theme["BG_COLOR"])
        
        self.observer = None
        self.current_geometry = design_config.LOGIN_WINDOW_SIZE
        
        self.setup_gui()
        if design_config.DEBUG:
            print("App initialized, checking for tampering")
        self.tamper_detector.check_for_tampering(self.root)

    def load_theme(self):
        theme_file = get_base_path() / ".theme_config.txt"
        if os.path.exists(theme_file):
            try:
                with open(theme_file, "r") as f:
                    theme = f.read().strip()
                    if theme == "light":
                        self.current_theme = design_config.LIGHT_THEME
                    else:
                        self.current_theme = design_config.DARK_THEME
                if design_config.DEBUG:
                    print(f"Loaded theme: {theme}")
            except Exception as e:
                if design_config.DEBUG:
                    print(f"Error loading theme: {e}")
                self.current_theme = design_config.DARK_THEME
        else:
            self.current_theme = design_config.DARK_THEME
            if design_config.DEBUG:
                print("No theme file found, defaulting to DARK_THEME")

    def save_theme(self):
        theme_file = get_base_path() / ".theme_config.txt"
        try:
            with open(theme_file, "w") as f:
                theme_name = "light" if self.current_theme == design_config.LIGHT_THEME else "dark"
                f.write(theme_name)
            set_hidden_attribute(theme_file)
            if design_config.DEBUG:
                print(f"Saved theme '{theme_name}' to {theme_file}")
        except Exception as e:
            if design_config.DEBUG:
                print(f"Error saving theme: {e}")

    def setup_gui(self):
        self.login_screen, self.master_password_entry = create_login_screen(self.root, self.login, self.current_language, self.current_theme, self.base_path)
        self.menu_screen = create_menu_screen(self.root, self.show_password_generator, self.show_password_manager, self.show_notes_manager, self.show_settings, self.logout, self.current_language, self.current_theme, self.base_path)
        self.password_generator_screen, self.length_slider, self.vars_dict, self.password_entry, self.strength_meter, self.length_label = create_password_generator_screen(
            self.root, self.back_to_menu, self.generate_password_callback, self.current_language, self.current_theme, self.base_path)
        self.password_manager_screen, self.website_entry, self.username_entry, self.password_manager_entry, self.password_tree, self.twofa_entry, self.tag_entry, self.search_entry = create_password_manager_screen(
            self.root, self.back_to_menu, self.add_password, self.delete_password, self.generate_password_for_manager, self.export_password, self.import_password, self.search_passwords, self.current_language, self.current_theme, self.base_path)
        self.notes_manager_screen, self.notes_tree, self.note_title_entry, self.note_text_editor = create_notes_manager_screen(
            self.root, self.back_to_menu, self.add_note, self.edit_note, self.delete_note, self.current_language, self.current_theme, self.base_path)
        self.settings_screen, self.new_password_entry, self.confirm_password_entry = create_settings_screen(
            self.root, self.back_to_menu, self.reset_master_password, self.update_language, self.clear_all_data, self.backup_data, self.restore_data, self.update_theme, self.current_language, self.current_theme, self.base_path)
        
        self.password_tree.bind("<Double-1>", self.reveal_password)
        self.password_tree.bind("<Button-1>", lambda event: self.copy_password(event) if self.password_tree.identify_column(event.x) == "#5" else None)
        self.notes_tree.bind("<<TreeviewSelect>>", self.load_selected_note)
        
        self.length_slider.bind("<B1-Motion>", lambda event: self.update_length_label(self.length_slider, self.length_label))
        self.length_slider.bind("<ButtonRelease-1>", lambda event: self.update_length_label(self.length_slider, self.length_label))
        
        self.login_screen.place(x=0, y=0, width=int(design_config.LOGIN_WINDOW_SIZE.split('x')[0]), height=int(design_config.LOGIN_WINDOW_SIZE.split('x')[1]))
        self.menu_screen.place(x=0, y=0, width=int(design_config.MENU_WINDOW_SIZE.split('x')[0]), height=int(design_config.MENU_WINDOW_SIZE.split('x')[1]))
        self.password_generator_screen.place(x=0, y=0, width=int(design_config.PASSWORD_GENERATOR_WINDOW_SIZE.split('x')[0]), height=int(design_config.PASSWORD_GENERATOR_WINDOW_SIZE.split('x')[1]))
        self.password_manager_screen.place(x=0, y=0, width=int(design_config.PASSWORD_MANAGER_WINDOW_SIZE.split('x')[0]), height=int(design_config.PASSWORD_MANAGER_WINDOW_SIZE.split('x')[1]))
        self.notes_manager_screen.place(x=0, y=0, width=int(design_config.NOTES_MANAGER_WINDOW_SIZE.split('x')[0]), height=int(design_config.NOTES_MANAGER_WINDOW_SIZE.split('x')[1]))
        self.settings_screen.place(x=0, y=0, width=int(design_config.SETTINGS_WINDOW_SIZE.split('x')[0]), height=int(design_config.SETTINGS_WINDOW_SIZE.split('x')[1]))
        
        self.login_screen.lift()

    def update_geometry(self, new_geometry):
        if self.current_geometry != new_geometry:
            self.root.geometry(new_geometry)
            self.current_geometry = new_geometry

    def refresh_gui(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        for screen in [self.login_screen, self.menu_screen, self.password_generator_screen, self.password_manager_screen, self.notes_manager_screen, self.settings_screen]:
            screen.destroy()
        self.root.configure(bg=self.current_theme["BG_COLOR"])
        self.setup_gui()
        if self.master_password:
            self.observer = start_file_monitoring(self.root, self.tamper_detector)

    def login(self, master_password_entry):
        current_time = time.time()
        if current_time - self.last_attempt_time < 5:
            messagebox.showerror("Error", "Too many attempts. Please wait.")
            return
        self.tamper_detector.check_for_tampering(self.root)
        password = master_password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a master password.")
            return
        hashed_password = hash_password(password)
        master_password_file = get_base_path() / ".master_password.txt"
        if design_config.DEBUG:
            print(f"Attempting to write master password to: {master_password_file}")
        try:
            if not os.path.exists(master_password_file):
                if design_config.DEBUG:
                    print("Setting new master password.")
                with open(master_password_file, "w") as file:
                    if design_config.DEBUG:
                        print(f"Opened {master_password_file} for writing")
                    file.write(hashed_password)
                    if design_config.DEBUG:
                        print(f"Wrote hashed password to {master_password_file}")
                if os.path.exists(master_password_file):
                    if design_config.DEBUG:
                        print(f"Master password file created at: {master_password_file}")
                else:
                    if design_config.DEBUG:
                        print(f"Failed to verify creation of {master_password_file}")
                self.tamper_detector.store_checksum(master_password_file, get_base_path() / ".master_password_checksum.txt")
                messagebox.showinfo("Success", "Master password set successfully.")
                self.master_password = password
                self.show_menu()
                if not self.observer:
                    self.observer = start_file_monitoring(self.root, self.tamper_detector)
            else:
                if not is_portable_data_present():
                    if design_config.DEBUG:
                        print("Portable data not found, resetting.")
                    messagebox.showwarning("Warning", "Portable data not found. Starting fresh.")
                    with open(master_password_file, "w") as file:
                        file.write(hashed_password)
                    if design_config.DEBUG:
                        print(f"Master password file reset at: {master_password_file}")
                    self.tamper_detector.store_checksum(master_password_file, get_base_path() / ".master_password_checksum.txt")
                    self.master_password = password
                    self.show_menu()
                    if not self.observer:
                        self.observer = start_file_monitoring(self.root, self.tamper_detector)
                elif not self.tamper_detector.verify_checksum(master_password_file, get_base_path() / ".master_password_checksum.txt"):
                    if design_config.DEBUG:
                        print("Checksum verification failed in login.")
                    self.tamper_detector.handle_tampering(self.root)
                    return
                else:
                    with open(master_password_file, "r") as file:
                        stored_password = file.read().strip()
                    if hashed_password == stored_password:
                        if design_config.DEBUG:
                            print("Login successful.")
                        self.master_password = password
                        self.show_menu()
                        if not self.observer:
                            self.observer = start_file_monitoring(self.root, self.tamper_detector)
                    else:
                        self.failed_attempts += 1
                        if self.failed_attempts >= 3:
                            self.tamper_detector.handle_tampering(self.root)
                        else:
                            messagebox.showerror("Error", "Incorrect master password.")
                            self.last_attempt_time = current_time
        except Exception as e:
            if design_config.DEBUG:
                print(f"Error during login/file creation: {e}")
            messagebox.showerror("Error", f"Failed to set master password: {e}")
        master_password_entry.delete(0, tk.END)

    def show_login(self):
        self.update_geometry(design_config.LOGIN_WINDOW_SIZE)
        self.login_screen.lift()

    def show_menu(self):
        if not self.tamper_detector.verify_checksum(get_base_path() / ".master_password.txt", get_base_path() / ".master_password_checksum.txt"):
            if design_config.DEBUG:
                print("Checksum verification failed in show_menu.")
            self.tamper_detector.handle_tampering(self.root)
            return
        self.update_geometry(design_config.MENU_WINDOW_SIZE)
        self.menu_screen.lift()

    def show_password_generator(self):
        self.update_geometry(design_config.PASSWORD_GENERATOR_WINDOW_SIZE)
        self.password_generator_screen.lift()
        self.toggle_strength_meter()

    def show_password_manager(self):
        self.update_geometry(design_config.PASSWORD_MANAGER_WINDOW_SIZE)
        self.password_manager_screen.lift()
        self.refresh_password_list()

    def show_notes_manager(self):
        self.update_geometry(design_config.NOTES_MANAGER_WINDOW_SIZE)
        self.notes_manager_screen.lift()
        self.refresh_notes_list()

    def show_settings(self):
        self.update_geometry(design_config.SETTINGS_WINDOW_SIZE)
        self.settings_screen.lift()

    def back_to_menu(self):
        self.update_geometry(design_config.MENU_WINDOW_SIZE)
        self.menu_screen.lift()

    def logout(self):
        self.master_password = None
        self.show_login()

    def reset_master_password(self, new_password_entry, confirm_password_entry):
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        hashed_password = hash_password(new_password)
        master_password_file = get_base_path() / ".master_password.txt"
        with self.tamper_detector:
            with open(master_password_file, "w") as file:
                file.write(hashed_password)
            self.tamper_detector.store_checksum(master_password_file, get_base_path() / ".master_password_checksum.txt")
            passwords = load_passwords(self.master_password)
            if passwords:
                save_passwords(passwords, new_password)
            notes = load_notes(self.master_password)
            if notes:
                save_notes(notes, new_password)
        self.master_password = new_password
        messagebox.showinfo("Success", "Master password reset successfully.")
        new_password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
        self.logout()

    def update_language(self, new_language):
        if new_language != self.current_language:
            self.current_language = new_language
            self.refresh_gui()

    def update_theme(self, new_theme):
        if new_theme == "dark":
            self.current_theme = design_config.DARK_THEME
        elif new_theme == "light":
            self.current_theme = design_config.LIGHT_THEME
        self.save_theme()
        self.refresh_gui()

    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data? This cannot be undone."):
            self.tamper_detector.handle_tampering(self.root)

    def update_slider_state(self):
        if self.vars_dict['apple'].get():
            self.length_slider.set(18)
            self.length_slider.config(state='disabled')
            self.length_label.config(text="Password Length: 18")
        else:
            self.length_slider.config(state='normal')
            self.length_slider.set(12 if self.length_slider.get() == 18 else self.length_slider.get())
            self.length_label.config(text=f"Password Length: {int(self.length_slider.get())}")

    def generate_password_callback(self, slider, vars_dict, entry, meter, length_label):
        length = 18 if vars_dict['apple'].get() else int(slider.get())
        password = generate_password(
            length,
            vars_dict['lowercase'].get(),
            vars_dict['uppercase'].get(),
            vars_dict['digits'].get(),
            vars_dict['symbols'].get(),
            vars_dict['exclude'].get(),
            vars_dict['apple'].get()
        )
        if password:
            entry.delete(0, tk.END)
            entry.insert(0, password)
            if vars_dict['strength'].get():
                meter.config(value=calculate_password_strength(password))
        length_label.config(text=f"Password Length: {length}")
        self.update_slider_state()

    def update_length_label(self, slider, label):
        if not self.vars_dict['apple'].get():
            label.config(text=f"Password Length: {int(slider.get())}")

    def generate_password_for_manager(self):
        password = generate_password(
            int(self.length_slider.get()),
            self.vars_dict['lowercase'].get(),
            self.vars_dict['uppercase'].get(),
            self.vars_dict['digits'].get(),
            self.vars_dict['symbols'].get(),
            self.vars_dict['exclude'].get(),
            self.vars_dict['apple'].get()
        )
        if password:
            self.password_manager_entry.delete(0, tk.END)
            self.password_manager_entry.insert(0, password)
            self.update_password_strength(self.password_manager_entry.get())

    def add_password(self, website_entry, username_entry, password_entry, twofa_entry, tag_entry):
        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        twofa_secret = twofa_entry.get() or ""
        tag = tag_entry.get() or "Uncategorized"
        if not all([website, username, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        passwords = load_passwords(self.master_password)
        passwords[website] = {
            "username": username,
            "password": password,
            "2fa_secret": twofa_secret,
            "tag": tag,
            "last_updated": time.time()
        }
        with self.tamper_detector:
            save_passwords(passwords, self.master_password)
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        twofa_entry.delete(0, tk.END)
        tag_entry.delete(0, tk.END)
        self.refresh_password_list()

    def delete_password(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a password to delete.")
            return
        website = tree.item(selected, "values")[0]
        passwords = load_passwords(self.master_password)
        if website in passwords:
            del passwords[website]
            with self.tamper_detector:
                save_passwords(passwords, self.master_password)
            self.refresh_password_list()

    def refresh_password_list(self, search_query=""):
        for row in self.password_tree.get_children():
            self.password_tree.delete(row)
        passwords = load_passwords(self.master_password)
        for website, creds in passwords.items():
            if search_query.lower() in website.lower() or search_query.lower() in creds["username"].lower():
                last_updated = creds.get("last_updated", 0)
                days_old = (time.time() - last_updated) / (60 * 60 * 24)
                expired = "⚠️" if days_old > 90 else ""
                totp = pyotp.TOTP(creds.get("2fa_secret", "")) if creds.get("2fa_secret") else None
                twofa_code = totp.now() if totp else "N/A"
                self.password_tree.insert("", "end", values=(
                    website, creds["username"], "*" * len(creds["password"]), creds["tag"], "📋", twofa_code, expired
                ))
        self.root.after(30000, lambda: self.refresh_password_list(search_query))

    def reveal_password(self, event):
        item = self.password_tree.identify_row(event.y)
        if item:
            values = self.password_tree.item(item, "values")
            if values[2] == "*" * len(values[2]):
                passwords = load_passwords(self.master_password)
                self.password_tree.set(item, column="Password", value=passwords[values[0]]["password"])
                self.root.after(10000, lambda: self.password_tree.set(item, column="Password", value="*" * len(values[2])))

    def copy_password(self, event):
        item = self.password_tree.identify_row(event.y)
        if item:
            passwords = load_passwords(self.master_password)
            website = self.password_tree.item(item, "values")[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(passwords[website]["password"])
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def toggle_strength_meter(self):
        if self.vars_dict['strength'].get():
            self.strength_meter.pack(pady=10, before=self.password_generator_screen.winfo_children()[-4])
        else:
            self.strength_meter.pack_forget()

    def update_password_strength(self, password):
        strength, _ = analyze_password_strength(password)
        color = "green" if strength >= 80 else "yellow" if strength >= 40 else "red"
        self.password_manager_screen.strength_label.config(text=f"Strength: {strength}%", fg=color)

    def export_password(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a password to export.")
            return
        website = tree.item(selected, "values")[0]
        passwords = load_passwords(self.master_password)
        passphrase = simpledialog.askstring("Passphrase", "Enter a passphrase for export:", show="*")
        if passphrase:
            with self.tamper_detector:
                export_file = export_password({website: passwords[website]}, passphrase)
            messagebox.showinfo("Success", f"Password exported to {export_file}")

    def import_password(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        passphrase = simpledialog.askstring("Passphrase", "Enter the passphrase to import:", show="*")
        if file_path and passphrase:
            try:
                with self.tamper_detector:
                    import_password(file_path, passphrase, self.master_password)
                self.refresh_password_list()
                messagebox.showinfo("Success", "Password imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import password: {e}")

    def search_passwords(self, query):
        self.refresh_password_list(query)

    def backup_data(self):
        with self.tamper_detector:
            backup_file = backup_data(self.master_password)
        messagebox.showinfo("Success", f"Backup created at {backup_file}")

    def restore_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Backup", "*.enc")])
        if file_path:
            with self.tamper_detector:
                restore_data(self.master_password, file_path)
                self.tamper_detector.store_checksum(get_base_path() / ".master_password.txt", get_base_path() / ".master_password_checksum.txt")
            messagebox.showinfo("Success", "Data restored successfully.")
            self.refresh_gui()

    def add_note(self, title_entry, text_editor):
        title = title_entry.get()
        content = text_editor.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showerror("Error", "Please enter a title and content.")
            return
        notes = load_notes(self.master_password)
        tags = {
            "bold": bool(text_editor.tag_ranges("bold")),
            "italic": bool(text_editor.tag_ranges("italic")),
            "underline": bool(text_editor.tag_ranges("underline")),
            "red": bool(text_editor.tag_ranges("red")),
            "blue": bool(text_editor.tag_ranges("blue")),
            "black": bool(text_editor.tag_ranges("black")),
            "bullet": bool(text_editor.tag_ranges("bullet"))
        }
        notes[title] = {"content": content, "tags": tags}
        with self.tamper_detector:
            save_notes(notes, self.master_password)
        title_entry.delete(0, tk.END)
        text_editor.delete("1.0", tk.END)
        self.refresh_notes_list()

    def edit_note(self, tree, title_entry, text_editor):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a note to edit.")
            return
        old_title = tree.item(selected, "values")[0]
        new_title = title_entry.get()
        content = text_editor.get("1.0", tk.END).strip()
        if not new_title or not content:
            messagebox.showerror("Error", "Please enter a title and content.")
            return
        notes = load_notes(self.master_password)
        if old_title in notes:
            del notes[old_title]
        tags = {
            "bold": bool(text_editor.tag_ranges("bold")),
            "italic": bool(text_editor.tag_ranges("italic")),
            "underline": bool(text_editor.tag_ranges("underline")),
            "red": bool(text_editor.tag_ranges("red")),
            "blue": bool(text_editor.tag_ranges("blue")),
            "black": bool(text_editor.tag_ranges("black")),
            "bullet": bool(text_editor.tag_ranges("bullet"))
        }
        notes[new_title] = {"content": content, "tags": tags}
        with self.tamper_detector:
            save_notes(notes, self.master_password)
        title_entry.delete(0, tk.END)
        text_editor.delete("1.0", tk.END)
        self.refresh_notes_list()

    def delete_note(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a note to delete.")
            return
        title = tree.item(selected, "values")[0]
        notes = load_notes(self.master_password)
        if title in notes:
            del notes[title]
            with self.tamper_detector:
                save_notes(notes, self.master_password)
            self.refresh_notes_list()

    def refresh_notes_list(self):
        for row in self.notes_tree.get_children():
            self.notes_tree.delete(row)
        notes = load_notes(self.master_password)
        for title in notes.keys():
            self.notes_tree.insert("", "end", values=(title,))

    def load_selected_note(self, event):
        selected = self.notes_tree.selection()
        if not selected:
            return
        title = self.notes_tree.item(selected, "values")[0]
        notes = load_notes(self.master_password)
        if title in notes:
            self.note_title_entry.delete(0, tk.END)
            self.note_title_entry.insert(0, title)
            self.note_text_editor.delete("1.0", tk.END)
            self.note_text_editor.insert("1.0", notes[title]["content"])
            tags = notes[title]["tags"]
            if tags.get("bold"):
                self.note_text_editor.tag_add("bold", "1.0", tk.END)
            if tags.get("italic"):
                self.note_text_editor.tag_add("italic", "1.0", tk.END)
            if tags.get("underline"):
                self.note_text_editor.tag_add("underline", "1.0", tk.END)
            if tags.get("red"):
                self.note_text_editor.tag_add("red", "1.0", tk.END)
            if tags.get("blue"):
                self.note_text_editor.tag_add("blue", "1.0", tk.END)
            if tags.get("black"):
                self.note_text_editor.tag_add("black", "1.0", tk.END)
            if tags.get("bullet"):
                lines = self.note_text_editor.get("1.0", tk.END).splitlines()
                self.note_text_editor.delete("1.0", tk.END)
                for line in lines:
                    self.note_text_editor.insert(tk.END, f"• {line}\n")
                    self.note_text_editor.tag_add("bullet", "insert linestart", "insert lineend")

    def run(self):
        self.root.mainloop()
        if self.observer:
            self.observer.stop()
            self.observer.join()

if __name__ == "__main__":
    app = KeyForgeApp()
    app.run()