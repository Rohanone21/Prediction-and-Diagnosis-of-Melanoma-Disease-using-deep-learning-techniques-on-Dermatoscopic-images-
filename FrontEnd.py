import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import sys


# Function to open a specific Python script in a new window
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


# Dictionary mapping button labels to their corresponding Python script files
script_mapping = {
    "Register": "final Reg.py",
    "Login": "Login from1.py",
    "Melanoma Detection": "GUI_Master.py",
    "Webcam Photo": "PhotoClicking.py",
    "Phone Photo": "PhonePhotoclicking.py",
    "Area Severity Detection": "AreaSeverityDetection.py",
    "Lesion Parameters": "ImageParameters.py",
    "Database": "Selected_database.py",
    "Precautions": "precautions.py",
    "Severity Analysis": "AreaSeverityDetection.py",
    "Skin Detection": "SkinDetection.py",
    "Generate Report": "ReportGeneration.py"
}

# Create the main window
root = tk.Tk()
root.title("Melanoma Diagnosis System")
root.attributes('-fullscreen', True)  # Enable Fullscreen

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and set background image
bg_image_path = "C:/Users/Rohan/Desktop/PythonProjects/skin cancer Desktop 100% code/img1.jpg"
if not os.path.exists(bg_image_path):
    messagebox.showerror("Error", "Background image not found!")
    sys.exit()

bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Add a project title at the top middle
title_label = tk.Label(root,
                       text="Prediction and Diagnosis of Melanoma Disease\nUsing Deep Learning Techniques on Dermatoscopic Images with CNN and U-NET Algorithms",
                       font=("Arial", 18, "bold"), bg="lightblue", fg="black", padx=10, pady=10)
title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)  # Positioned at the top middle

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="white", bd=2)
button_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # Adjusted for better centering

# Create and place buttons with corresponding script names
buttons = []
for idx, (btn_label, script_name) in enumerate(script_mapping.items()):
    def make_lambda(script=script_name):
        return lambda: open_script(script)


    btn = tk.Button(button_frame, text=btn_label, width=25, height=2, font=("Arial", 14, "bold"), command=make_lambda())
    btn.grid(row=idx // 4, column=idx % 4, padx=20, pady=20)  # 4 columns per row
    buttons.append(btn)


# Exit fullscreen on pressing "Esc"
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)


root.bind("<Escape>", exit_fullscreen)  # Allow exiting fullscreen with "Esc" key

# Run the application
root.mainloop()
