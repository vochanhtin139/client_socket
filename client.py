# from calendar import leapdays
from ast import Global
from asyncio.windows_events import NULL
from base64 import encode
from cmath import exp
from email import message
from tkinter.ttk import *
from tkinter import *
from socket import *
import json
from turtle import width 
from PIL import Image, ImageTk 
import sqlite3
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

FORMAT = "utf-8"

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

def decreaseNum(i):
    global numOfFood
    global num
    if numOfFood[i] == 0:
        return
    numOfFood[i] = numOfFood[i] - 1
    num[i].config(text=str(numOfFood[i]))

def increaseNum(i):
    global numOfFood
    global num
    numOfFood[i] = numOfFood[i] + 1
    num[i].config(text=str(numOfFood[i]))

def add_item(qq, i, item, pic):
    global numOfFood
    global dec
    global num
    global inc

    frame = Frame(qq, highlightbackground="grey", bg = a, highlightthickness=1, bd=0)
    frame.pack(side=LEFT, anchor=NE, expand=TRUE, fill=BOTH)
    # frame.grid(row=2, column=i)

    img = Image.open(BytesIO(pic))
    img.thumbnail((200, 200), Image.ANTIALIAS)
    imgTk = ImageTk.PhotoImage(img)

    lb = Label(frame, image=imgTk, width=200, height=200, bg=a)
    lb.pack(fill=BOTH)
    frame.image = imgTk

    if len(item['food_name']) > 24:
        food_name = item['food_name'][0:20]
        food_name = food_name + '...'
    else:
        food_name = item['food_name']
    name = Label(frame, text=food_name, bg=a, fg='white', font=('Calibri (Body)', 15, 'bold'), anchor=N)
    name.pack(fill=BOTH) 

    if len(item['description']) > 28:
        description = item['description'][0:24]
        description = description + '...'
    else:
        description = item['description']
    des = Label(frame, text=description, bg=a, fg='white', font=('Calibri (Body)', 13), anchor=N)
    des.pack(fill=BOTH) 

    price = Label(frame, text=str(item['price']) + 'đ', bg=a, fg='white', font=('Calibri (Body)', 15, 'bold'), anchor=N)
    price.pack(fill=BOTH) 


    # Decrease number
    dec[i] = Button(frame, text='-', bd=2, fg=a, bg='white', relief=GROOVE, font=('Calibri (Body)', 16, 'bold'), pady=5, padx=10, command=lambda: decreaseNum(i))
    dec[i].pack(side=LEFT)

    # Current number
    num[i] = Label(frame, text=str(numOfFood[i]), bg='white', fg='black', font=('Calibri (Body)', 16), pady=10)
    num[i].pack(side=LEFT, expand=TRUE, fill=X)

    # Increase number
    inc[i] = Button(frame, text='+', bd=2, fg=a, bg='white', relief=GROOVE, font=('Calibri (Body)', 16, 'bold'), pady=5, padx=8, command=lambda: increaseNum(i))
    inc[i].pack(side=LEFT)

dec = []
num = []
inc = []
numOfFood = []

# Add food to menu
def add_food(q):
    h1 = Label(q, text='Client Menu', fg='pink', bg=a, font=('Forte', 35), pady=12)
    h1.pack(fill=BOTH)

    jData_length = sck.recv(1024).decode(FORMAT)
    sck.sendall(jData_length.encode(FORMAT))
    jData = sck.recv(int(jData_length)).decode(FORMAT)
    sck.sendall(jData.encode(FORMAT))
    jArr = json.loads(jData)
    
    sendStr = "Received"
    
    for i in range(len(jArr)):
        numOfFood.append(0)
        dec.append(Label())
        num.append(Label())
        inc.append(Label())

    # Create a canvas
    canvas = Canvas(q, bg=a)
    canvas.pack(fill=BOTH, expand=TRUE)

    # Add a scrollbar to the canvas
    scr = Scrollbar(q, orient=HORIZONTAL, bg=a, command=canvas.xview)
    scr.pack(side=BOTTOM, fill=BOTH)

    # Configure the canvas
    canvas.configure(xscrollcommand=scr.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    

    # Create another frame inside the canvas
    qq = Frame(canvas)

    # Add that new frame to a window in the canvas
    canvas.create_window((0,0), window=qq, anchor=NW)

    img = []
    for i in range(len(jArr)-1):
    # for i in range(7):
        imgRecv_length = sck.recv(1024).decode(FORMAT)
        sck.sendall(sendStr.encode(FORMAT))
        imgRecv = sck.recv(int(imgRecv_length))
        sck.sendall(sendStr.encode(FORMAT))

        img.append(imgRecv)
        tfood = "food" + str(i + 1)
        add_item(qq, i + 1, jArr[i + 1][tfood], imgRecv)

    submit = Button(q, text="Đặt món")

# New window after splash screen
def new_win():
    q = Tk()
    q.title("")
    q.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
    Frame(q, width=857, height=482, bg=a).place(x=0, y=0)

    add_food(q)

    q.mainloop()

# Config the bar at splash screen
def bar():
    tmp = inputPort.get()
    print(value.get())
    if value.get() != "":
        l4 = Label(w, text='Loading...', fg="white", bg=a, anchor=S)
        lst4 = ('Calibri (Body)', 10)
        l4.config(font=lst4)
        l4.pack(side=LEFT, pady=(50, 0))

        import time
        r = 0
        for i in range(100):
            progress['value'] = r
            w.update_idletasks()
            time.sleep(0.02)
            r = r + 1

        sck.sendall(str(len(value.get())).encode(FORMAT))
        sck.recv(1024)
        sck.sendall(value.get().encode(FORMAT))
        sck.recv(1024)
    
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