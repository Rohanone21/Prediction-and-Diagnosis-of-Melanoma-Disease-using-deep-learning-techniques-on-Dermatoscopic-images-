import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys

# Function to open a specific Python script in a new window (from code1)
def open_script(script_name):
    try:
        script_path = os.path.abspath(script_name)  # Get the full path of the script
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"File not found: {script_path}")
            return
        subprocess.Popen([sys.executable, script_path],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)  # Open in new console
    except Exception as e:
        messagebox.showerror("Error", f"Could not open {script_name}\n{str(e)}")


# GUI Window (from code2)
root = tk.Tk()
root.title("Melanoma Detection System")
root.geometry("1000x600")
root.configure(bg="lightblue")

# Project Title
project_title = "Prediction and Diagnosis of Melanoma Disease using Deep Learning Techniques on Dermatoscopic Images with CNN and U-NET Algorithms"
title_label = tk.Label(root, text=project_title, font=("Arial", 14, "bold"), bg="lightblue", wraplength=800,
                       justify="center")
title_label.pack(pady=10)

# Function to Get Patient Info (from code2)
def get_patient_info():
    patient_name = name_entry.get()
    patient_age = age_entry.get()

    # Display on Top Left
    patient_name_label.config(text=f"Name: {patient_name}")
    patient_age_label.config(text=f"Age: {patient_age}")
    input_window.destroy()

# Create Input Window for Name and Age (from code2)
input_window = tk.Toplevel(root)
input_window.title("Patient Information")
input_window.geometry("300x150")

tk.Label(input_window, text="Enter Patient Name:", font=("Arial", 10, "bold")).pack()
name_entry = tk.Entry(input_window, font=("Arial", 10))
name_entry.pack(pady=5)

tk.Label(input_window, text="Enter Patient Age:", font=("Arial", 10, "bold")).pack()
age_entry = tk.Entry(input_window, font=("Arial", 10))
age_entry.pack(pady=5)

tk.Button(input_window, text="Submit", font=("Arial", 10, "bold"), command=get_patient_info).pack(pady=10)

# Frame for Patient Info (Top Left) (from code2)
patient_info_frame = tk.Frame(root, bg="lightblue")
patient_info_frame.place(x=20, y=20)

tk.Label(patient_info_frame, text="Patient Details", font=("Arial", 12, "bold"), bg="lightblue").pack()

patient_name_label = tk.Label(patient_info_frame, text="Name: ", font=("Arial", 10, "bold"), bg="lightblue")
patient_name_label.pack()
patient_age_label = tk.Label(patient_info_frame, text="Age: ", font=("Arial", 10, "bold"), bg="lightblue")
patient_age_label.pack()

# Frame for Buttons (from code2)
button_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
button_frame.pack(pady=20)

# Load Icons (from code2)
icon_size = (40, 40)
icons = {
    "Melanoma Detection": "images.jpeg",
    "Webcam Photo": "camera.webp",
    "Phone Photo": "phone.png",
    "Area Severity Detection": "severity.png",
    "Lesion Parameters": "lesion.png",
    "Database": "database.png",
    "Precautions": "precaution.png",
    "Skin Detection": "skin.png",
    "Generate Report": "report.png",
}

# Corresponding Python Modules (from code2)
modules = {
    "Melanoma Detection": "GUI_Master.py",
    "Webcam Photo": "PhotoClicking.py",
    "Phone Photo": "PhonePhotoclicking.py",
    "Area Severity Detection": "AreaSeverityDetection.py",
    "Lesion Parameters": "ImageParameters.py",
    "Database": "Selected_database.py",
    "Precautions": "precautions.py",
    "Skin Detection": "SkinDetection.py",
    "Generate Report": "ReportGeneration.py"
}

# Function to Create Buttons (from code2)
def create_button(frame, text, icon_file, row, col):
    if os.path.exists(icon_file):
        img = Image.open(icon_file).resize(icon_size)
        img = ImageTk.PhotoImage(img)
        btn = tk.Button(frame, text=text, image=img, compound="top", font=("Arial", 10, "bold"), bd=2, relief="solid",
                        command=lambda: open_script(modules[text]))  # Use open_script from code1
        btn.image = img  # Keep reference
        btn.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)
    else:
        btn = tk.Button(frame, text=text, font=("Arial", 10, "bold"), bd=2, relief="solid",
                        command=lambda: open_script(modules[text]))  # Use open_script from code1
        btn.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)

# Arrange Buttons in Grid (from code2)
button_list = list(icons.keys())
for i, btn_text in enumerate(button_list):
    create_button(button_frame, btn_text, icons[btn_text], i // 3, i % 3)

# Run GUI (from code2)
root.mainloop()

