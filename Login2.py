import tkinter as tk
from tkinter import messagebox

# Sample Patient Data
PATIENT_DATA = {"user1": {"name": "Rohan", "age": 21}}

# Function to Handle Login
def login():
    username = entry_username.get()

    if username in PATIENT_DATA:
        name = PATIENT_DATA[username]['name']
        age = PATIENT_DATA[username]['age']

        # Save Name & Age in a File
        with open("user_data.txt", "w") as f:
            f.write(f"{name},{age}")

        messagebox.showinfo("Login Successful", "Login successful! Now open the main GUI.")
        root.destroy()  # Close Login Window
    else:
        messagebox.showerror("Login Failed", "Invalid Username!")

# GUI Window
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Enter Username:", font=("Arial", 12)).pack(pady=10)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5)
tk.Button(root, text="Login", font=("Arial", 12), command=login).pack(pady=10)

root.mainloop()
