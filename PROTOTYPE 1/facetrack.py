import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create a database connection and table if it doesn't exist
def initialize_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 first_name TEXT NOT NULL,
                 last_name TEXT NOT NULL,
                 birthday TEXT NOT NULL,
                 address TEXT NOT NULL,
                 contact_info TEXT NOT NULL,
                 student_id TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        messagebox.showinfo("Login Info", f"Logged in as {username}")
    else:
        messagebox.showwarning("Login Info", "Invalid username or password")

# Function to handle registration submission
def submit_registration():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    birthday = entry_birthday.get()
    address = entry_address.get()
    contact_info = entry_contact_info.get()
    student_id = entry_student_id.get()
    username = entry_username.get()
    password = entry_password.get()
    
    summary = f"""
    Username: {username}
    Password: {password}
    First Name: {first_name}
    Last Name: {last_name}
    Birthday: {birthday}
    Address: {address}
    Contact Info: {contact_info}
    Student ID: {student_id}
    """
    
    if messagebox.askyesno("Confirm Registration", f"Is this information correct?\n{summary}"):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, first_name, last_name, birthday, address, contact_info, student_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (username, password, first_name, last_name, birthday, address, contact_info, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration Info", f"Registered as {username}")
        registration_window.destroy()

# Function to handle registration
def register():
    global entry_first_name, entry_last_name, entry_birthday, entry_address, entry_contact_info, entry_student_id, registration_window
    
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    tk.Label(registration_window, text="First Name:").grid(row=0, column=0)
    entry_first_name = tk.Entry(registration_window)
    entry_first_name.grid(row=0, column=1)

    tk.Label(registration_window, text="Last Name:").grid(row=1, column=0)
    entry_last_name = tk.Entry(registration_window)
    entry_last_name.grid(row=1, column=1)

    tk.Label(registration_window, text="Birthday:").grid(row=2, column=0)
    entry_birthday = tk.Entry(registration_window)
    entry_birthday.grid(row=2, column=1)

    tk.Label(registration_window, text="Address:").grid(row=3, column=0)
    entry_address = tk.Entry(registration_window)
    entry_address.grid(row=3, column=1)

    tk.Label(registration_window, text="Contact Info:").grid(row=4, column=0)
    entry_contact_info = tk.Entry(registration_window)
    entry_contact_info.grid(row=4, column=1)

    tk.Label(registration_window, text="Student ID:").grid(row=5, column=0)
    entry_student_id = tk.Entry(registration_window)
    entry_student_id.grid(row=5, column=1)

    tk.Button(registration_window, text="Submit", command=submit_registration).grid(row=6, columnspan=2)

# Create the main window
root = tk.Tk()
root.title("Login and Registration")

# Create and place the username and password labels and entries
tk.Label(root, text="Username:").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=1, column=1)

# Create and place the login and register buttons
tk.Button(root, text="Login", command=login).grid(row=2, column=0)
tk.Button(root, text="Register", command=register).grid(row=2, column=1)

# Initialize the database
initialize_db()

# Run the main loop
root.mainloop()
