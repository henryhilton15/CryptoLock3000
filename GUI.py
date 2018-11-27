try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    
import tkinter.messagebox as box

def dialog1():
    username=entry1.get()
    password = entry2.get()
    if (username == 'admin' and  password == 'secret'):
        box.showinfo('info','Correct Login')
    else:
        box.showinfo('info','Invalid Login')


window = Tk()
window.title('Countries Generation')

frame = Frame(window)

Label1 = Label(window,text = 'Username:')
Label1.pack(padx=15,pady= 5)

entry1 = Entry(window,bd =5)
entry1.pack(padx=15, pady=5)



Label2 = Label(window,text = 'Password: ')
Label2.pack(padx = 15,pady=6)

entry2 = Entry(window, bd=5)
entry2.pack(padx = 15,pady=7)




btn = Button(frame, text = 'Check Login',command = dialog1)
