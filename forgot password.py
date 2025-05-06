from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.configure(background='#85BB65')
root.geometry("1920x1080+0+0")  # Set resolution to 1920x1080

# Background image setup
image2 = Image.open('s3.webp')
image2 = image2.resize((1920, 1080), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Database setup
db = sqlite3.connect('skin.db')
cursor = db.cursor()
cursor.execute("""
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

# Variables for input
email = tk.StringVar()
password = tk.StringVar()
confirmPassword = tk.StringVar()

# Labels and Entry fields
email_label = tk.Label(
    root, text='Email', font=('Cambria', 14), background='#85BB65'
).place(x=500, y=180)
email_entry = tk.Entry(
    root, width=40, textvariable=email, background='#ffffff'
).place(x=730, y=180)

password_label = tk.Label(
    root, text='New Password', font=('Cambria', 14), background='#85BB65'
).place(x=500, y=280)
password_entry = tk.Entry(
    root, width=40, textvariable=password, background='#ffffff'
).place(x=730, y=280)

confirm_password_label = tk.Label(
    root, text='Confirm Password', font=('Cambria', 14), background='#85BB65'
).place(x=500, y=315)
confirm_password_entry = tk.Entry(
    root, width=40, show="*", textvariable=confirmPassword, background='#ffffff'
).place(x=730, y=315)

# Change password function
def change_password():
    new_password = password.get()
    confirm_password = confirmPassword.get()

    with sqlite3.connect('skin.db') as db:
        c = db.cursor()
        find_user = 'SELECT * FROM registration WHERE Email=?'
        c.execute(find_user, [(email.get())])
        result = c.fetchall()

        if result:
            if new_password == confirm_password:
                c.execute("UPDATE registration SET password=? WHERE Email=?", (new_password, email.get()))
                db.commit()
                ms.showinfo('Success', 'Password changed successfully')
                root.destroy()
            else:
                ms.showerror('Error', "Passwords didn't match")
        else:
            ms.showerror('Error', 'Email not found in the database')

# Submit button
submit_button = tk.Button(
    root, text="Send", width=10, command=change_password, background='#85BB65'
)
submit_button.place(x=850, y=390)

# Run the application
root.mainloop()
