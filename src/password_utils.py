# src/password_utils.py
import hashlib
import random
import string
from tkinter import messagebox

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_password(length, lowercase, uppercase, digits, symbols, exclude_similar, apple_formatting):
    try:
        if apple_formatting:
            length = 18
        elif length < 4:
            raise ValueError("Password length must be at least 4 characters.")
        
        character_sets = []
        if lowercase:
            character_sets.append(string.ascii_lowercase)
        if uppercase:
            character_sets.append(string.ascii_uppercase)
        if digits:
            character_sets.append(string.digits)
        if symbols and not apple_formatting:
            character_sets.append(string.punctuation)

        if not character_sets:
            raise ValueError("Please select at least one character type.")

        all_characters = ''.join(character_sets)
        
        if exclude_similar:
            similar_characters = "il1Lo0O"
            all_characters = ''.join([char for char in all_characters if char not in similar_characters])

        password = [random.choice(all_characters) for _ in range(length)]
        random.shuffle(password)
        password = ''.join(password)

        if apple_formatting:
            password = '-'.join([password[i:i+6] for i in range(0, len(password), 6)])
        
        return password
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None

def calculate_password_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(char.islower() for char in password):
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char in string.punctuation for char in password):
        strength += 1
    return strength * 20

def analyze_password_strength(password):
    details = {
        "length": len(password),
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(c in string.punctuation for c in password)
    }
    strength = calculate_password_strength(password)
    return strength, details