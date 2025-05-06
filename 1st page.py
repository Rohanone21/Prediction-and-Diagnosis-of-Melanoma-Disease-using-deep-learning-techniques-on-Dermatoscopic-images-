import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import os

# Initialize the root window
root = tk.Tk()
root.configure(background='white')

# Set the screen resolution to 1920x1080
root.geometry("1920x1080+0+0")
root.title("Melanoma Skin Cancer Detection")

# Check if the image file exists
if os.path.exists("s1.jpeg"):
    # Load and resize the background image
    image2 = Image.open("s1.jpeg")
    image2 = image2.resize((1920, 1080), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)

    # Display the background image
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image  # Keep a reference to prevent garbage collection
    background_label.place(x=0, y=0)
else:
    print("Error: File 's1.jpeg' not found. Background image will not be displayed.")

# Header Label
header_label = tk.Label(
    root, text="Melanoma Skin Cancer Detection", font=("Calibri", 40, "bold"),
    bg="light gray", fg="black", width=60, height=2
)
header_label.place(x=0, y=0)

# Login Button Function
def log():
    from subprocess import call
    call(['python', 'Login from1.py'])

# Login Button
login_button = tk.Button(
    root, text="Login", command=log, font=("Arial", 18, "bold"),
    width=10, height=1, bd=2, bg="light gray", fg="black"
)
login_button.place(x=1400, y=30)

# Register Button Function
def reg():
    from subprocess import call
    call(['python', 'final Reg.py'])

# Register Button
register_button = tk.Button(
    root, text="Register", command=reg, font=("Arial", 18, "bold"),
    width=10, height=1, bd=2, bg="light gray", fg="black"
)
register_button.place(x=1550, y=30)

# Information Text
info_text = (
    "Melanoma skin care is a set of practices that can improve the appearance of your skin,\n"
    "relieve skin conditions, and support the integrity of your skin.\n"
    "\n"
    "Here are some tips for healthy skin:\n"
    "- Cleanse: Wash your face gently with warm water and a mild cleanser.\n"
    "- Protect from the sun: Avoid intense sun exposure and use sunscreen.\n"
    "- Moisturize: Use gentle moisturizers, lotions, or creams to prevent dry skin.\n"
    "- Hydrate: Drink plenty of water to stay hydrated.\n"
    "- Reduce stress: Stress can harm your skin, so try to keep it in check.\n"
    "- Sleep: Get enough sleep, which is about 7-8 hours a night for adults.\n"
    "- Exfoliate: Remove dead skin cells to brighten your complexion.\n"
    "- Monitor your skin: Talk to your doctor if you notice any changes to your skin.\n"
)
info_label = tk.Label(
    root, text=info_text, font=('Cambria', 18), bg='white', fg='black', justify="left"
)
info_label.place(x=100, y=150)

# Link to Open in Browser
def open_browser():
    webbrowser.open("https://www.practo.com/pune/treatment-for-skin-cancer-screening")

# Browser Link
link_label = tk.Label(
    root, text="Learn more about skin cancer detection and care",
    font=('Arial', 14, 'underline'), fg="blue", bg="white", cursor="hand2"
)
link_label.place(x=700, y=700)
link_label.bind("<Button-1>", lambda e: open_browser())

# Start the application
root.mainloop()
