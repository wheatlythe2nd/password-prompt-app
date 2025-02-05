import bcrypt
import hashlib
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os
from tkinter import Tk, Label, messagebox
from PIL import Image, ImageTk
from PIL.Image import Resampling  # Add this import
import subprocess

# Path to the file where user data will be stored
USER_DATA_FILE = 'user_data.json'

def load_user_data():
    """Load user data from the JSON file."""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Return an empty dictionary if the file is empty or contains invalid JSON
            return {}
    return {}

def save_user_data(user_data):
    """Save user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def hash_username(username):
    """Hash a username using SHA-256."""
    return hashlib.sha256(username.encode()).hexdigest()

def create_username():
    """Create a new username and store the hashed username and password."""
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty")
        return
    
    user_data = load_user_data()
    hashed_username = hash_username(username)
    if (hashed_username in user_data):
        messagebox.showerror("Error", "Username already exists")
        return
    
    hashed_password = hash_password(password)
    user_data[hashed_username] = hashed_password.decode()
    save_user_data(user_data)
    messagebox.showinfo("Success", "Username created successfully")
    create_button.pack_forget()  # Hide create button after successful creation

def hide_login():
    input_frame.place_forget()  # Hide login frame

def show_login():
    input_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show login frame
    logout_frame.place_forget()  # Hide logout button
    hide_gif()

def verify_password():
    """Verify the entered password against the stored hashed password."""
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty")
        return
    
    user_data = load_user_data()
    hashed_username = hash_username(username)
    
    if hashed_username not in user_data:
        messagebox.showerror("Error", "Username does not exist")
        return
    
    stored_hashed_password = user_data[hashed_username].encode()
    if bcrypt.checkpw(password.encode(), stored_hashed_password):
        messagebox.showinfo("Success", "Password verified successfully")
        hide_login()
        show_logout_button()
        show_gif()
    else:
        messagebox.showerror("Error", "Incorrect password")

def show_logout_button():
    logout_frame.place(relx=0.5, rely=0.9, anchor="center")

def clear_user_data():
    """Clear the user data file."""
    if os.path.exists(USER_DATA_FILE):
        os.remove(USER_DATA_FILE)
        messagebox.showinfo("Success", "User data file cleared")
        create_button.pack(pady=5)  # Show create button
    else:
        messagebox.showerror("Error", "User data file does not exist")

def resize_image(event=None):
    width = window.winfo_width()
    height = window.winfo_height()
    
    # Replace ANTIALIAS with Resampling.LANCZOS
    image = original_image.resize((width, height), Resampling.LANCZOS)
    global photo
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

def enforce_aspect_ratio(event=None):
    if event and event.widget == window:
        width = window.winfo_width()
        height = window.winfo_height()
        if abs(width - height) > 2:
            new_size = min(width, height)
            x = window.winfo_x()
            y = window.winfo_y()
            window.geometry(f"{new_size}x{new_size}+{x}+{y}")

def check_existing_user():
    """Check if any user exists and update UI accordingly"""
    user_data = load_user_data()
    if user_data:
        create_button.pack_forget()
    else:
        create_button.pack(pady=5)

def show_gif():
    """Display animated GIF after login"""
    gif_label.place(relx=0.5, rely=0.5, anchor="center")

def hide_gif():
    """Hide GIF when logging out"""
    gif_label.place_forget()

def launch_online():
    """Launch the online.py program"""
    subprocess.Popen(['python', 'online.py'])

def show_success():
    """Show success message for debugging"""
    messagebox.showinfo("Debug", "Success!")

def create_gui():
    global username_entry, password_entry, original_image, label, window, photo, input_frame, logout_frame, create_button, gif_label
    
    window = tk.Tk()
    window.title("Password Manager")
    window.geometry("800x800")
    
    # Load original image at full resolution without initial resize
    original_image = Image.open("girl with gun.png")
    photo = ImageTk.PhotoImage(original_image)
    label = tk.Label(window, image=photo)
    label.pack(fill="both", expand=True)
    
    # Separate bindings for smoother updates
    window.bind("<Configure>", enforce_aspect_ratio)
    window.bind("<Configure>", resize_image)
    
    # Create login frame
    input_frame = tk.Frame(window, bg="white")
    input_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Create logout frame
    logout_frame = tk.Frame(window, bg="white")
    tk.Button(logout_frame, text="Logout", command=show_login).pack(pady=5)
    tk.Button(logout_frame, text="Go Online", command=show_success).pack(pady=5)
    
    # Create and place the input fields and buttons
    tk.Label(input_frame, text="Enter your username:", bg="white").pack(pady=5)
    username_entry = tk.Entry(input_frame)
    username_entry.pack(pady=5)

    tk.Label(input_frame, text="Enter your password:", bg="white").pack(pady=5)
    password_entry = tk.Entry(input_frame, show='*')
    password_entry.pack(pady=5)

    create_button = tk.Button(input_frame, text="Create Username", command=create_username)
    verify_button = tk.Button(input_frame, text="Verify Password", command=verify_password)
    clear_button = tk.Button(input_frame, text="Clear User Data", command=clear_user_data)
    
    # Check for existing user before showing create button
    check_existing_user()
    verify_button.pack(pady=5)
    clear_button.pack(pady=5)
    
    # Create GIF label with animation
    gif = Image.open("hatsune-miku-dance.gif")
    frames = []
    try:
        while True:
            # Convert to RGBA for transparency
            frame = gif.convert('RGBA')
            photoframe = ImageTk.PhotoImage(frame)
            frames.append(photoframe)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    gif_label = tk.Label(window)
    gif_label.frames = frames  # Keep reference
    
    def update_gif(frame_index=0):
        frame = frames[frame_index]
        gif_label.configure(image=frame)
        next_frame = (frame_index + 1) % len(frames)
        # Adjust timing (40ms = ~25fps)
        window.after(40, update_gif, next_frame)
    
    update_gif()  # Start animation
    
    # Start the GUI event loop
    window.mainloop()

if __name__ == '__main__':
    create_gui()
