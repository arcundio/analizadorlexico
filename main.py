from tkinter import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

def analizar():
    print(token.get())   

root = Tk()
root.geometry("600x600")
frame = Frame(root)
frame.pack()
 
label = Label(frame, text = "Ingrese el token")
label.pack()

token = Entry(frame, width = 20)
token.pack(padx = 5, pady = 5)

button = Button(frame, text= "Analizar", command=analizar)
button.pack()
 
root.title("Analizador Léxico")
root.mainloop()