from tkinter import *
import qrcode
import tkinter.messagebox as tmsg
from pyqrcode import create
import pyqrcode
import os

#! Body of the GUI
root=Tk()
root.geometry("555x555")
root.minsize(555,555)
# root.maxsize(555,555)

root.wm_iconbitmap("C:\\Users\\91762\\Desktop\\VS Code\\Projects\\qrgen\\icon.ico")
root.title("QR Code Generator--- By Deepraj")

#@ Defining Global Variables

myQr=""
photo=""

#^Logic
def click():
    if len(scvalue.get())!=0:
        global myQr
        myQr=pyqrcode.create(scvalue.get())
        global photo
        qrImage=myQr.xbm(scale=6)
        photo=BitmapImage(data=qrImage)
        
    else:
        tmsg.showerror("Link Empty","The link You entered is either Invalid or Empty")
    try:
        showCode()
    except:
        tmsg.showwarning("ERROR","Something went wrong Please Check the Link You Entered")
    
def showCode():
	global photo
	notificationLabel.config(image= photo)
	subLabel.config(text= f"QR Code Generated for:\n{screen.get()[:15].upper()}...",font="consolas 13 bold",fg="#E52D28")
    

def clear():
    scvalue.set("")
    screen.update()

scvalue=StringVar()
scvalue.set("")

notificationLabel= Label(root)
subLabel= Label(root, text="")
notificationLabel.pack()
subLabel.pack()

f1=Frame(root,bg="#CFAF2D",borderwidth=5,height=7,width=20)
name=Label(f1,text="Paste your Link Here ⬇",font="Consolas 18",fg="#EE601D")
name.pack(padx=4,pady=1,ipadx=20,fill=X)
f1.pack(padx=4,pady=1,ipadx=20,fill=X)

screen=Entry(root,textvar=scvalue,font="Consolas 16",bg="#B5BABA",relief=SUNKEN)
screen.pack(side=TOP,fill=X,padx=20,pady=10)

f2=Frame(root,bg="#B5BABA", height=325,width=325)
b=Button(f2,text="Clear",font="Consolas 18",bg="#E66A50",width=10,command=clear)
b.pack(side=RIGHT,padx=4,pady=3)

b=Button(f2,text="Get QR Code",font="Consolas 18",bg="#E66A50",width=11,command=click)
b.pack(side=RIGHT,padx=4,pady=3)
# b.bind('<Button-1>')

# b.bind('<Button-1>')
f2.pack()

root.mainloop()