
#!Updating GUI size with given user Input.

from tkinter import *
import tkinter.messagebox as tmsg

#?Creating function for the Button

def update():
    root.geometry(f"{height.get()}x{width.get()}")
    tmsg.showinfo("Resizing the GUI",f"Your GUI size Changed to {height.get()} x {width.get()}")

root=Tk()
root.geometry("345x245")
root.title("Deepraj's GUI")
f1=Frame(root,bg="#E4E46C",borderwidth=10,relief=SUNKEN)
f1.pack(padx=20,pady=10)
txt=Label(f1,text="GUI RESIZER",font="hack 20 bold").pack(anchor=N)

#? creating variables to take input from the user
width=StringVar()
height=StringVar()

#!Creating widgets to take entries
text1=Label(root,text="Enter the Height",font="Consolas 15")
text1.pack()
Entry(root,textvariable=width).pack()

text2=Label(root,text="Enter the Width",font="Consolas 15")
text2.pack()
Entry(root,textvariable=height).pack()

#!Creating Button
Button(root,text="Aply\nChanges",command=update,font="hack 14").pack(padx=5)


root.mainloop()