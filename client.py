# from calendar import leapdays
from ast import Global
from cmath import exp
from tkinter.ttk import *
from tkinter import *
from socket import *
import json 
from PIL import Image, ImageTk 
import sqlite3
from io import BytesIO

# *********************************** 
# *         Initialize SOCKET       *
# ***********************************

sck = socket(AF_INET, SOCK_STREAM)
sck.connect(("127.0.0.1", 9000))

# *********************************** 
# *          Initialize GUI         *
# ***********************************

# Initialize height and weight of windows
w = Tk()

w.title("")

width_of_window = 854
height_of_window = 500
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

# w.overrideredirect(1)

s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background="#4f4f4f")
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=1000, mode='determinate')

def decreaseNum(num, numOfFood):
    numOfFood = numOfFood - 1
    num.config(text=str(numOfFood))

def increaseNum(num, numOfFood):
    numOfFood = numOfFood + 1
    num.config(text=str(numOfFood))

def add_item(q, i, item, pic):
    frame = Frame(q, highlightbackground="grey", bg = a, highlightthickness=1, width = 200, height = 200, bd=0)
    # frame.pack(side=LEFT, anchor=NE, expand=TRUE)
    frame.pack(side=LEFT)

    img = Image.open(BytesIO(pic))
    img.thumbnail((200, 200), Image.ANTIALIAS)
    imgTk = ImageTk.PhotoImage(img)

    lb = Label(frame, image=imgTk, width=200, height=200, bg=a)
    lb.pack(fill=BOTH)
    frame.image = imgTk

    des = item['food_name'] + '\n' + item['description'] + '\n' + str(item['price'])
    name = Label(frame, text=des, bg=a, fg='white')
    name.pack(fill=BOTH)     

    # Decrease number
    dec[i] = Button(frame, text='-', bd=0, fg=a, bg='white', font=('Calibri (Body)', 18, 'bold'), pady=5, padx=5, command=lambda: decreaseNum(num[i], numOfFood[i]))
    dec[i].pack(side=LEFT)

    # Current number
    num[i] = Label(frame, text=str(numOfFood), bg='white', fg=a, font=('Calibri (Body)', 18), padx=30, pady=5)
    num[i].pack(side=LEFT, expand=TRUE, fill=BOTH)

    # Increase number
    inc[i] = Button(frame, text='+', bd=0, fg=a, bg='white', font=('Calibri (Body)', 18, 'bold'), pady=5, padx=5, command=lambda: increaseNum(num[i], numOfFood[i]))
    inc[i].pack(side=LEFT)

# Add food to menu
def add_food(q):
    h1 = Label(q, text='CLIENT MENU', fg='green', bg=a, font=('Calibri (Body)', 30, 'bold'))
    h1.pack(fill=BOTH)

    jData = sck.recv(100000)
    # print(jData)
    jArr = json.loads(jData.decode())
    # print(jArr)

    sendStr = "Received"
    sck.send(sendStr.encode())

    global numOfFood
    global dec
    global num
    global inc
    dec = []
    num = []
    inc = []
    numOfFood = []
    for i in range(len(jArr)):
        numOfFood.append(0)
        dec.append(Label())
        num.append(Label())
        inc.append(Label())


    img = []
    # if (jArr[0]['type'] == 'food_menu'):
    for i in range(len(jArr) - 1):
        imgRecv = sck.recv(100000)
        img.append(imgRecv)
        tfood = "food" + str(i + 1)
        if i < 2:
            add_item(q, i + 1, jArr[i+1][tfood], imgRecv)

    # imgTmp = Image.open(BytesIO(img[5]))
    # imgTk = ImageTk.PhotoImage(imgTmp)
    # lb = Label(q, image=imgTk)
    # lb.pack() 
    # q.image = imgTk

# New window after splash screen
def new_win():
    q = Tk()
    q.title("")
    q.geometry("854x500")
    Frame(q, width=857, height=482, bg=a).place(x=0, y=0)

    # l1 = Label(q, text='ADD TEXT HERE ', fg='grey', bg=None)
    # l = ('Calibri (Body)', 24, 'bold')
    # l1.config(font=l)
    # l1.pack(expand=TRUE)

    # tmp = inputPort.get()
    # print(value.get())
    # sck.sendall(value.get().encode())

    add_food(q)

    q.mainloop()

# Config the bar at splash screen
def bar():
    l4 = Label(w, text='Loading...', fg="white", bg=a, anchor=S)
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    # l4.place(x=18, y=210)
    l4.pack(side=LEFT, pady=(50, 0))

    import time
    r = 0
    for i in range(100):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.02)
        r = r + 1

    w.destroy()
    new_win()

progress.pack(side=BOTTOM)

# Adding widget at splash screen
a = '#249794'
Frame(w, width=857, height=482, bg = a).place(x=0, y=0)

l1 = Label(w, text='CLIENT MENU', fg = 'white', bg=a, anchor=W)
lst1 = ('Courier New', 50, 'bold italic')
l1.config(font=lst1)
# l1.place(x=90, y=50)
l1.pack(fill=BOTH, padx=100, pady=(50, 0))

l2 = Label(w, text="Group 08", fg="white", bg=a, anchor=W)
lst2 = ('Tahoma', 28)
l2.config(font=lst2)
# l2.place(x=90, y=110)
l2.pack(fill=BOTH, padx=100)

l3 = Label(w, text="Vo Chanh Tin\nPhan Nhu Quynh\nNguyen Van Dang Huynh", foreground="white", background=a, justify=LEFT, anchor=W)
lst3 = ('Tahoma', 14)
l3.config(font=lst3)
l3.pack(fill=BOTH, padx=100, pady=10)

l4 = Label(w, text="Enter table ID:", bg=a, fg="white")
l4.pack(pady=(10, 0))

value = StringVar()
inputPort = Entry(w, bg="white", justify=CENTER, textvariable=value)
inputPort.configure(font=("Tahoma", 20))
# inputPort.bind('<Return>', bar)
inputPort.pack()

b1 = Button(w, width=20, height=2, text="Get started", command=lambda: bar(), border=1, fg=a, bg="white", anchor=CENTER)
b1.pack(pady=50)
w.mainloop()