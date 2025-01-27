import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate a random password
def generate_password():
    try:
        length = length_slider.get()
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4 characters.")
            return

        # Define character sets based on checkbox selections
        character_sets = []
        if lowercase_var.get():
            character_sets.append(string.ascii_lowercase)
        if uppercase_var.get():
            character_sets.append(string.ascii_uppercase)
        if digits_var.get():
            character_sets.append(string.digits)
        if symbols_var.get() and not apple_formatting_var.get():  # Exclude symbols for Apple formatting
            character_sets.append(string.punctuation)

        # Check if at least one character set is selected
        if not character_sets:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        # Combine selected character sets
        all_characters = ''.join(character_sets)

        # Generate the password
        password = []
        for _ in range(length):
            password.append(random.choice(all_characters))

        # Shuffle the password to make it more random
        random.shuffle(password)

        # Convert the list to a string
        password = ''.join(password)

        # Apply Apple formatting if enabled
        if apple_formatting_var.get():
            if length != 18:
                messagebox.showerror("Error", "Apple formatting requires a password length of 18.")
                return
            password = '-'.join([password[i:i+6] for i in range(0, len(password), 6)])

        # Display the password
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length.")

# Function to copy the password to the clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password generated yet.")

# Function to update the password length label
def update_length_label(value):
    length_label.config(text=f"Password Length: {int(value)}")

# Function to handle the selection of extra features
def handle_extra_features(choice):
    if choice == "Apple Formatting":
        apple_formatting_var.set(True)
        symbols_var.set(False)  # Disable symbols for Apple formatting
        symbols_check.config(state=tk.DISABLED)
        length_slider.set(18)  # Set length to 18 for Apple formatting
        length_slider.config(state=tk.DISABLED)  # Disable the slider
    else:
        apple_formatting_var.set(False)
        symbols_check.config(state=tk.NORMAL)
        length_slider.config(state=tk.NORMAL)  # Re-enable the slider

# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x400")

# Label to display the selected password length
length_label = tk.Label(root, text="Password Length: 12")
length_label.pack(pady=5)

# Slider for password length
length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, length=300, showvalue=0, command=update_length_label)
length_slider.set(12)  # Default password length
length_slider.pack(pady=5)

# Checkboxes for character types
lowercase_var = tk.BooleanVar(value=True)
lowercase_check = tk.Checkbutton(root, text="Include Lowercase Letters", variable=lowercase_var)
lowercase_check.pack(pady=2)

uppercase_var = tk.BooleanVar(value=True)
uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var)
uppercase_check.pack(pady=2)

digits_var = tk.BooleanVar(value=True)
digits_check = tk.Checkbutton(root, text="Include Digits", variable=digits_var)
digits_check.pack(pady=2)

symbols_var = tk.BooleanVar(value=True)
symbols_check = tk.Checkbutton(root, text="Include Symbols", variable=symbols_var)
symbols_check.pack(pady=2)

# Drop-down menu for extra features
extra_features_var = tk.StringVar(value="None")
extra_features_label = tk.Label(root, text="Extra Features:")
extra_features_label.pack(pady=5)

extra_features_menu = tk.OptionMenu(root, extra_features_var, "None", "Apple Formatting", command=handle_extra_features)
extra_features_menu.pack(pady=5)

# Variable to track Apple formatting
apple_formatting_var = tk.BooleanVar(value=False)

# Button to generate password
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=10)

# Label and entry to display the generated password
password_label = tk.Label(root, text="Generated Password:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, width=30)
password_entry.pack(pady=5)

# Button to copy password to clipboard
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=10)

# Run the application
root.mainloop()