import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import CNNModel 
from keras import optimizers
import sqlite3
from tensorflow.keras.optimizers import SGD
global fn
fn=""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="seashell2")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Skin Cancer Detection ")



bg = Image.open("s6.jpg")

# bg.resize((1366,500),Image.ANTIALIAS)
# print(w,h)
bg_img = ImageTk.PhotoImage(bg)
bg_lbl = tk.Label(root, image=bg_img)
bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

frame_alpr = tk.LabelFrame(root, text=" --Process-- ", width=280, height=900, font=('times', 14, ' bold '),bg="grey")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=0, y=0)

# calling the function
def shift():
    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): #reset the coordinates
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

canvas=tk.Canvas(root,bg="black")
canvas.pack()
canvas.place(x=0, y=0)
text_var="Melanoma Skin Cancer Detection "
text=canvas.create_text(0,-2000,text=text_var,font=('Raleway',25,'bold'),fill='white',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = 1600
height = 50
canvas['width']=width
canvas['height']=height
fps=40    #Change the fps to make the animation faster/slower
shift()   #Function Calli

# Create a function to retrieve the selected item from the drop-down list
def get_selected_item():
    selected_item = combobox.get()  # Get the selected item from the Combobox
    print(selected_item)
    #label.config(text=f"Selected Item: {selected_item}")  # Update the label text with the selected item
    if (selected_item=='Actinic keratosis'):
        label=tk.Label(root,text=''' Actinic keratosis:''',width=40,font=('times',20,'bold'),bg="white",fg="black")
        label.place(x=700,y=100)
        label=tk.Label(root,text='''                       
        Protect your skin from the sun:\n
        Avoid the sun between 10 AM and 2 PM, when UV rays are strongest  \n
Wear sunscreen with at least SPF 30 on all exposed skin, including your lips  \n
Reapply sunscreen every two hours, or more often if you're sweating or swimming  \n
Wear protective clothing like long-sleeved shirts, long pants, and a wide-brimmed hat  \n
Avoid tanning beds, sun lamps, and tanning salons  \n
Check your skin regularly :\n
Examine your skin head to toe for new growths or changes to moles, freckles, bumps, and birthmarks \n
Report any changes to your doctor
        
        ''',width=90,bg="black",fg="white",height=33)
        label.place(x=700,y=200)
        
    elif (selected_item=='Nevus'):
        label=tk.Label(root,text='''Nevus:''',width=40,font=('times',20,'bold'),bg="white",fg="black")
        label.place(x=700,y=100)
        label=tk.Label(root,text='''
        precautions:\n
        Use a broad-spectrum sunscreen with a skin protection factor (SPF) of 30 or higher. ...\n
Wear hats with wide brims to protect your face and ears.\n
Wear long-sleeved shirts and pants to protect your arms and legs. ...\n
Wear sunglasses to protect your eyes.''',bg="black",fg="white",width=90,height=33)
        label.place(x=700,y=200)
        
   
         
         
    elif (selected_item=='Melanoma'):
         label=tk.Label(root,text=''' Melanoma: ''',width=40,font=('times',20,'bold'),bg="white",fg="black")
         label.place(x=700,y=100)
         label=tk.Label(root,text='''
         precautions::\n
         Avoid Sunburns: Stay out of the sun during peak hours (10 AM to 4 PM) when UV rays are strongest.\n
Wear Sunscreen: Use a broad-spectrum sunscreen with an SPF of 30 or higher.\n Reapply every two hours and after swimming or sweating.\n
Protective Clothing: Wear long-sleeved shirts, wide-brimmed hats, and sunglasses with UV protection.\n
Seek Shade: Use umbrellas or sit under trees when outdoors''',bg="black",fg="white",width=90,height=33)
         label.place(x=700,y=200)
        
         
   

# Create a Label
label = tk.Label(frame_alpr, text='''       Select an Item:         ''',font=('times',15, ' bold '),bg="white",fg="black",height=2,bd=5)
label.place(x=30,y=150)

# Create a Combobox (Drop-down list)
options = ['Actinic keratosis','Nevus','Melanoma']  # List of options
selected_option = tk.StringVar()  # Variable to hold selected item
combobox = ttk.Combobox(frame_alpr, textvariable=selected_option, values=options, state="readonly",font=('times',15, ' bold '))
combobox.place(x=30,y=250)

# Create a Button to get the selected item
button = tk.Button(root, text=" Get Selected Item ", command=get_selected_item,width=15, height=2, font=('times', 15, ' bold '),bg="white",fg="black")
button.place(x=30,y=500)




#################################################################################################################
def window():
    root.destroy()



# button2 = tk.Button(frame_alpr, text="Amla", command=Amla, width=20, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
# button2.place(x=10, y=70)




exit = tk.Button(frame_alpr, text="Exit", command=window, width=15, height=1, font=('times', 15, ' bold '),bg="black",fg="white")
exit.place(x=30, y=700)



root.mainloop()

