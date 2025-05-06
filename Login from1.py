import tkinter as tk
import sqlite3
from tkinter import messagebox as ms
from PIL import Image, ImageTk
from tkinter.ttk import *

# Initialize the main window
root = tk.Tk()
root.configure(background='#73A16C')

# Set the screen resolution to 1920x1080
root.geometry("1920x1080+0+0")
root.title("Melanoma Skin Cancer Detection")

# Load and set the background image
image2 = Image.open('s4.jpg')
image2 = image2.resize((1920, 1080), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image  # Keep a reference to prevent garbage collection
background_label.place(x=0, y=0)

# Variables for user inputs
Email = tk.StringVar()
password = tk.StringVar()

# Login Function
def login():
    with sqlite3.connect('skin.db') as db:
        c = db.cursor()
        # Create the table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS registration (
                name TEXT, 
                address TEXT,  
                Email TEXT, 
                country TEXT, 
                Phoneno TEXT, 
                Gender TEXT, 
                password TEXT
            )
        """)
        db.commit()

        # Check if credentials match
        find_entry = 'SELECT * FROM registration WHERE Email = ? AND password = ?'
        c.execute(find_entry, [(Email.get()), (password.get())])
        result = c.fetchall()

        if result:
            ms.showinfo("Message", "Login successful")
            from subprocess import call
            call(['python', 'GUI_Master.py'])
        else:
            ms.showerror('Error', 'Username or Password not found/matched.')

# Forgot Password Function
def forgot():
    from subprocess import call
    call(['python', 'forgot password.py'])

# Registration Function
def reg():
    from subprocess import call
    call(['python', 'final reg.py'])

# Header Label
header_label = tk.Label(
    root, text="Melanoma Skin Cancer Detection", font=("Calibri", 40, "bold"),
    bg="#e4b7a0", width=60, height=1
)
header_label.place(x=0, y=0)

# Login Section
login_label = tk.Label(root, text='Login Here', fg='black', bg='#e4b7a0', font=('Forte', 25))
login_label.place(x=230, y=200)

# Login Canvas
canvas1 = tk.Canvas(root, border=0, background="#e4b7a0")
canvas1.place(x=50, y=280, width=500, height=400)

# Email and Password Labels and Entry Boxes
email_label = tk.Label(root, text='Enter Email', bg='#e4b7a0', font=('Cambria', 14))
email_label.place(x=120, y=400)

password_label = tk.Label(root, text='Enter Password', bg='#e4b7a0', font=('Cambria', 14))
password_label.place(x=120, y=450)

email_entry = tk.Entry(root, width=40, textvariable=Email, bg='#e4b7a0')
email_entry.place(x=270, y=400)

password_entry = tk.Entry(root, width=40, show='*', textvariable=password, bg='#e4b7a0')
password_entry.place(x=270, y=450)

# Forgot Password Button
forgot_button = tk.Button(root, text="Forgot Password?", fg='blue', bg='#e4b7a0', command=forgot)
forgot_button.place(x=400, y=500)

# Login Button
login_button = tk.Button(root, text="Login", font=("Bold", 9), command=login, width=50, bg='#e4b7a0')
login_button.place(x=130, y=560)

# Sign-Up Section
not_member_label = tk.Label(root, text='Not a Member?', font=('Cambria', 11), bg='#e4b7a0')
not_member_label.place(x=350, y=657)

signup_button = tk.Button(root, text="Sign Up", fg='blue', bg='#e4b7a0', command=reg)
signup_button.place(x=450, y=653, width=55)

# Start the GUI event loop
root.mainloop()
