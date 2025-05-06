import tkinter as tk
import sqlite3
import random
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import re

# Create the main window
root = tk.Tk()
root.configure(background='white')
w, h = 1920, 1080  # Set resolution to 1920x1080
root.geometry("%dx%d+0+0" % (w, h))

# Background Image
image2 = Image.open('s2.jpg')
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Variables for form fields
name = tk.StringVar()
address = tk.StringVar()
Email = tk.StringVar()
country = tk.StringVar()
PhoneNo = tk.IntVar()
var = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

# Database setup
db = sqlite3.connect('skin.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS registration"
               "(name TEXT, address TEXT, Email TEXT, country TEXT, Phoneno TEXT, Gender TEXT, password TEXT)")
db.commit()

# Password check function
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True
    if len(passwd) < 6:
        val = False
    if len(passwd) > 20:
        val = False
    if not any(char.isdigit() for char in passwd):
        val = False
    if not any(char.isupper() for char in passwd):
        val = False
    if not any(char.islower() for char in passwd):
        val = False
    if not any(char in SpecialSym for char in passwd):
        val = False
    return val

# Insert function to store data in the database
def insert():
    fname = name.get()
    addr = address.get()
    un = country.get()
    email = Email.get()
    mobile = PhoneNo.get()
    gender = var.get()
    pwd = password.get()
    cnpwd = password1.get()

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        email_valid = True
    else:
        email_valid = False

    if fname.isdigit() or fname == "":
        ms.showinfo("Message", "Please enter a valid name")
    elif addr == "":
        ms.showinfo("Message", "Please enter an address")
    elif email == "" or not email_valid:
        ms.showinfo("Message", "Please enter a valid email")
    elif len(str(mobile)) != 10:
        ms.showinfo("Message", "Please enter a 10-digit mobile number")
    elif un == "":
        ms.showinfo("Message", "Please enter a valid country")
    elif pwd == "" or not password_check(pwd):
        ms.showinfo("Message", "Password must contain at least 1 uppercase letter, 1 symbol, and 1 number")
    elif pwd != cnpwd:
        ms.showinfo("Message", "Password and confirm password must match")
    else:
        conn = sqlite3.connect('skin.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO registration(name, address, Email, country, Phoneno, Gender, password) VALUES(?,?,?,?,?,?,?)',
                           (fname, addr, email, un, mobile, gender, pwd))
            conn.commit()
            ms.showinfo('Success!', 'Account Created Successfully!')
            conn.close()
            from subprocess import call
            call(['python', 'Login from1.py'])

# UI Elements
label = tk.Label(root, text="Registration Form", font=("Forte", 30), bg="#87CEEB", fg="black")
label.place(x=180, y=90)

# Adjust position of the "Create Account" button relative to the label
label.update_idletasks()  # To get the updated size of the label
heading_width = label.winfo_width()  # Get the width of the heading

# Create Account Button on the right side of the heading
create_account_button = tk.Button(root, text="Create Account", font=("Arial", 11), width=15, command=insert, bg="#87CEEB", fg="black")
create_account_button.place(x=180 + heading_width + 20, y=90)

# Canvas for form fields
canvas = tk.Canvas(root, background="#87CEEB", borderwidth=5)
canvas.place(x=150, y=150, width=400, height=590)

# Add label function
def add_label(text, x, y):
    return tk.Label(root, text=text, font=("Calibri", 10), bg="#87CEEB").place(x=x, y=y)

# Add entry function
def add_entry(var, x, y, show=None):
    return tk.Entry(root, border=2, textvar=var, bg="#87CEEB", show=show).place(x=x, y=y)

# Form Labels and Fields
add_label("Name:", 200, 200)
add_entry(name, 330, 205)

add_label("Email:", 200, 250)
add_entry(Email, 330, 255)

add_label("Password:", 200, 300)
add_entry(password, 330, 305, show="*")

add_label("Re-Enter Password:", 200, 350)
add_entry(password1, 330, 355, show="*")

add_label("Address:", 200, 400)
add_entry(address, 330, 405)

add_label("Country:", 200, 450)
add_entry(country, 330, 455)

add_label("Phone no:", 200, 515)
add_entry(PhoneNo, 330, 520)

add_label("Gender:", 200, 590)
tk.Radiobutton(root, text="Male", font=("Calibri", 10), bg="#87CEEB", value=1, variable=var).place(x=330, y=590)
tk.Radiobutton(root, text="Female", font=("Calibri", 10), bg="#87CEEB", value=2, variable=var).place(x=400, y=590)

root.mainloop()
