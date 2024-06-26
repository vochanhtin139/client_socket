# from calendar import leapdays
from ast import Global
from cmath import exp
from distutils.log import info
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
import time
from datetime import datetime, timedelta
import datetime
import tkinter.messagebox as mbox
ImageFile.LOAD_TRUNCATED_IMAGES = True

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
height_of_window = 550
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

w.overrideredirect(1)

s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background="#4f4f4f")
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=1000, mode='determinate')

def decreaseNum(i):
    global numOfFood
    global num
    global exNum
    if numOfFood[i] == 0:
        return
    if numOfFood[i] == exNum[i]:
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

def updateOrder(q, paymentMethod, n, arr, btn_Submit):
    for i in range(n - 1):
        exNum[i + 1] = numOfFood[i + 1]
        
    btn_Submit.config(text="Cập nhật", command=lambda: orderFood(q, n, arr, btn_Submit, "update")) 

def check2hours(nowTime, exTime):
    if (nowTime - exTime).seconds <= 7200:
        return True
    return False

def sendOrder(n, arr, ord_OR_upd):
    if ord_OR_upd == "order":
        order = "Order Food"
        sck.sendall(str(len(order)).encode().ljust(64))
        sck.sendall(order.encode())
    else:
        update = "Update Food"
        sck.sendall(str(len(update)).encode().ljust(64))
        sck.sendall(update.encode())
        
    global exTimeOrder
    timeOrder = datetime.datetime.now()
    if ord_OR_upd == "update":
        if check2hours(timeOrder, exTimeOrder[0]) == False:
            mbox.showerror("Error", "Quá thời hạn cập nhật đơn hàng")
            sendStr = "false"
            sck.sendall(str(len(sendStr)).encode().ljust(64))
            sck.sendall(sendStr.encode())
            return False
        else:
            sendStr = "true"
            sck.sendall(str(len(sendStr)).encode().ljust(64))
            sck.sendall(sendStr.encode())
            
    tmp = {
            "type": "food_order"
        }
    jArr = []
    jArr.append(tmp)
    cnt = 1
    for i in range(n):
        if numOfFood[i + 1] > 0:
            tfood = "food" + str(cnt)
            js = {
                tfood: {
                    "id": str(arr[i+1]["food" + str(i + 1)]['id']),
                    "num": str(numOfFood[i+1]),
                    "price": str(arr[i + 1]["food" + str(i + 1)]['price'])
                }
            }
            jArr.append(js)
            cnt += 1
    
    # Send food order
    sck.sendall(str(len(json.dumps(jArr))).encode().ljust(64))
    sck.sendall(json.dumps(jArr).encode())
    
    # Send time order
    sck.sendall(str(len(str(timeOrder))).encode().ljust(64))
    sck.sendall(str(timeOrder).encode())

    exTimeOrder[0] = timeOrder
    return True
def sendPayment(cash, card):
    # Send cash
    sck.sendall(str(len(cash)).encode().ljust(64))
    sck.sendall(str(cash).encode())
    
    # Send card
    sck.sendall(str(len(card)).encode().ljust(64))
    sck.sendall(str(card).encode())
    
def orderFood(q, n, arr, btn_Submit, ord_OR_upd):
    # Check no food:
    flag = 1
    for i in range(n):
        if numOfFood[i+1] > 0:
            flag = 0
            break
    if flag == 1:
        return 
    
    # Send food order
    sendSucc = sendOrder(n, arr, ord_OR_upd)
    
    if sendSucc == False:
        return
    
    # Receive total
    sum_length = recvall(sck, 64).decode()
    sum = recvall(sck, int(sum_length)).decode()
    global exSum
    
    # print ("Current date and time = %s" % e)
    # print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))
    # print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    
    popup = Toplevel(q)
    popup.geometry("500x550+500+120")
    popup.title("Đơn hàng của bạn")

    set = Treeview(popup)
    set.pack()

    set['columns']= ('food_name', 'num', 'price', 'total')
    set.column("#0", width=0,  stretch=NO)
    set.column("food_name", width=160,  anchor=CENTER)
    set.column("num",anchor=CENTER, width=80)
    set.column("price",anchor=CENTER, width=120)
    set.column("total",anchor=CENTER, width=120)

    set.heading("#0",text="",anchor=CENTER)
    set.heading("food_name",text="Món",anchor=CENTER)
    set.heading("num",text="SL",anchor=CENTER)
    set.heading("price",text="Giá",anchor=CENTER)
    set.heading("total",text="Thành tiền",anchor=CENTER)

    for i in range(n):
        if numOfFood[i+1] > 0:
            tfood = "food" + str(i + 1)
            total = numOfFood[i+1] * int(arr[i+1][tfood]['price'])
            set.insert(parent='', index='end', iid=i, text='', values=(arr[i + 1][tfood]['food_name'], str(numOfFood[i + 1]), str(arr[i+1][tfood]['price']), str(total)))
        
    sumFrame = Frame(popup, pady=20)
    sumFrame.pack()
    if (ord_OR_upd == "order"):
        Label(sumFrame, text="Tổng: ", font=('Calibri (Body)', 18, 'bold')).pack(side=LEFT, padx=50)
        Label(sumFrame, text=str(sum), font=('Calibri (Body)', 18, 'bold')).pack(side=RIGHT, padx=50)
    else:
        Label(sumFrame, text="Tổng: ", font=('Calibri (Body)', 18, 'bold')).pack(side=LEFT, padx=50)
        Label(sumFrame, text=str(sum), font=('Calibri (Body)', 18, 'bold')).pack(side=RIGHT, padx=50)
        remainFrame = Frame(popup)
        remainFrame.pack()
        Label(remainFrame, text="Số tiền thanh toán thêm: ", font=('Calibri (Body)', 14, 'bold')).pack(side=LEFT, padx=20)
        Label(remainFrame, text=str(int(sum) - int(exSum[0])), font=('Calibri (Body)', 14, 'bold')).pack(side=RIGHT, padx=20)
# update payment
    paymentFrame = Frame(popup)
    paymentFrame.pack(pady=20, fill=BOTH)
    choice = IntVar()
    Label(paymentFrame, text="Phương thức thanh toán:", font=('Calibri (Body)', 16, 'underline')).pack(anchor=W, padx=20)
    if (ord_OR_upd == "order"):
        cash = Radiobutton(paymentFrame, text='Thanh toán tiền mặt', font=('Calibri (Body)', 15), variable=choice, value=0)
        cash.pack()
        card = Radiobutton(paymentFrame, text='Thanh toán bằng thẻ', font=('Calibri (Body)', 15), variable=choice, value=1)
        card.pack()
    else:
        if (exChoice[0] == 0):
            cash = Radiobutton(paymentFrame, text='Thanh toán tiền mặt', font=('Calibri (Body)', 15), variable=choice, value=0)
            cash.pack()
        else:
            card = Radiobutton(paymentFrame, text='Thanh toán bằng thẻ', font=('Calibri (Body)', 15), variable=choice, value=1)
            card.pack()
            
    Button(paymentFrame, text="Thanh toán", font=('Calibri (Body)', 16), relief=RAISED, command=lambda: payment(q, popup, choice.get(), n, arr, sum, btn_Submit)).pack(pady=20)
    
    popup.protocol("WM_DELETE_WINDOW", lambda: on_closing(popup))
    popup.mainloop()

def on_closing(popup):
    if mbox.askokcancel("Quit", "Bạn có muốn thoát không?"):
        quit = "Quit"
        sck.sendall(str(len(quit)).encode().ljust(64))
        sck.sendall(str(quit).encode())
        popup.destroy()

def payment(q, popup, choice, n, arr, sum, btn_Submit):
    global exChoice
    exChoice[0] = choice
    if choice == 1:
        infoCard = Toplevel(popup)
        infoCard.geometry("350x180+550+250")
        infoCard.title("Thông tin thanh toán")
        
        frame = Frame(infoCard,  width=350, height=180)
        frame.pack()
        Label(frame, text="Số thẻ: ", font=("Calibri (Body)", 15)).pack(side=LEFT, padx=20, pady=30)
        stk = StringVar()
        stkBox = Entry(frame, fg=a, bg="white", justify=CENTER, textvariable=stk, width=200)
        stkBox.configure(font=("Tahoma", 15))
        stkBox.pack(side=RIGHT, padx=20, pady=30)
        
        Button(infoCard, text="Xác nhận", relief=RAISED, font=("Calibri (Body)", 15), command=lambda: checkStk(q, popup, infoCard, stk.get(), n, arr, sum, btn_Submit)).pack()
        
        infoCard.mainloop()
    else:
        mbox.showinfo("Information", "Đặt món thành công")
        stk = ""
        sendPayment(sum, stk)
        popup.destroy()
        updateOrder(q, 0, n, arr, btn_Submit)
        
        global exSum
        exSum[0] = int(sum) 
        
def checkStk(q, popup, infoCard, stk, n, arr, sum, btn_Submit):
    sendPayment(sum, stk)
    flag_length = recvall(sck, 64).decode()
    flagRecv = recvall(sck, int(flag_length)).decode()
    
    if flagRecv == '0':
        mbox.showerror("Error", "Số thẻ không hợp lệ")
        infoCard.destroy()
    else:
        mbox.showinfo("Information", "Thanh toán thành công")
        infoCard.destroy()
        popup.destroy()
        updateOrder(q, 1, n, arr, btn_Submit)
        global exSum
        exSum[0] = int(sum) 
        
    
dec = []
num = []
inc = []
numOfFood = []
exNum = []
exTimeOrder = []
exSum = []
exChoice = []

# Add food to menu
def add_food(q, tID):
    h1 = Label(q, text='Client Menu', fg='pink', bg=a, font=('Forte', 35), pady=12)
    h1.pack(fill=BOTH)

    h2 = Label(q, text="ID bàn: " + tID, fg='white', bg=a, font=('Tahoma', 12, "bold"))
    h2.pack(pady=(0, 5))

    sendStr = "Received"

    length = recvall(sck, 64)
    length1 = length.decode('utf-8')
    jData = recvall(sck, int(length1))
    # jData = sck.recv(int(length.decode()))
    jArr = json.loads(jData.decode())
    
    n = len(jArr)

    exTimeOrder.append("")
    exSum.append(0)
    exChoice.append(0)
    for i in range(len(jArr)):
        numOfFood.append(0)
        exNum.append(0)
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
        length = recvall(sck, 64).decode('utf-8')
        imgRecv = recvall(sck, int(length))
        img.append(imgRecv)
        tfood = "food" + str(i + 1)
        add_item(qq, i + 1, jArr[i + 1][tfood], imgRecv)

    submit = Button(q, text="Đặt món", font=('Calibri (Body)', 15, 'bold'), command=lambda: orderFood(q, n-1, jArr, submit, "order"))
    submit.pack(pady=10)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# New window after splash screen
def new_win(tID):
    q = Tk()
    q.title("Client menu")
    q.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
    Frame(q, width=857, height=532, bg=a).place(x=0, y=0)

    add_food(q, tID)

    q.mainloop()

# Config the bar at splash screen
def bar():
    tmp = inputPort.get()
    if tmp != "":
        sck.sendall(str(len(value.get())).encode().ljust(64))
        sck.sendall(value.get().encode())
        l4 = Label(w, text='Loading...', fg="white", bg=a, anchor=S)
        lst4 = ('Calibri (Body)', 10)
        l4.config(font=lst4)
        # l4.place(x=18, y=210)
        l4.pack(side=LEFT, pady=(50, 0))

        r = 0
        for i in range(100):
            progress['value'] = r
            w.update_idletasks()
            time.sleep(0.02)
            r = r + 1

        w.destroy()
        new_win(tmp)

progress.pack(side=BOTTOM)

# Adding widget at splash screen
a = '#249794'
Frame(w, width=857, height=532, bg = a).place(x=0, y=0)

l1 = Label(w, text='CLIENT MENU', fg = 'white', bg=a, anchor=W)
lst1 = ('Courier New', 50, 'bold italic')
l1.config(font=lst1)
l1.pack(fill=BOTH, padx=100, pady=(50, 0))

l2 = Label(w, text="NHÓM 08", fg="white", bg=a, anchor=W)
lst2 = ('Tahoma', 28)
l2.config(font=lst2)
# l2.place(x=90, y=110)
l2.pack(fill=BOTH, padx=100)

l3 = Label(w, text="Võ Chánh Tín\nPhan Như Quỳnh\nNguyễn Văn Đăng Huỳnh", foreground="white", background=a, justify=LEFT, anchor=W)
lst3 = ('Tahoma', 14)
l3.config(font=lst3)
l3.pack(fill=BOTH, padx=100, pady=10)

l4 = Label(w, text="Nhập table ID:", bg=a, fg="white")
l4.pack(pady=(10, 0))

value = StringVar()
inputPort = Entry(w, bg="white", justify=CENTER, textvariable=value)
inputPort.configure(font=("Tahoma", 20))
# inputPort.bind('<Return>', bar)
inputPort.pack()

b1 = Button(w, width=20, height=2, text="Bắt đầu", command=lambda: bar(), border=1, fg=a, bg="white", anchor=CENTER)
b1.pack(pady=50)
w.mainloop()