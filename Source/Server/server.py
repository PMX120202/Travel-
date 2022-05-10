import tkinter as tk
import socket
from tkinter import *
import tkinter
import threading
import json
import os.path
#Khai bao socket va cac thong tin



HOST="127.0.0.1"
SERVER_PORT=65432
FORMAT="utf8"

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,SERVER_PORT))

location=[]
clientList = []

# Load tat ca thong tin dang co trong json vao mang location
with open('data.json') as json_file:
    location = json.load(json_file)
# Ham gui hinh anh cho client
def Gui_Anh_Client(imageID, clientAddress):
    file = open(imageID,  "rb")

    while True:
        Anh = file.read(2048)
        s.sendto(Anh, clientAddress)
        if not Anh:
            s.sendto(Anh, clientAddress)
            break
        # s.sendto(Anh, clientAddress)
    file.close()
# Thread xu li gui thong tin cho client
def Client_Thread():
    print("The server is ready to receive") 
    while 1:
    #Bat dau nhan yeu cau ben client
        msg,clientAddress=s.recvfrom(2048)
        clientList.append(clientAddress)
        print(clientAddress)
        print(msg.decode())
        if msg.decode()=="full":
            
            s.sendto(str(len(location)).encode(),clientAddress)

            for i in location:
                s.sendto(i["Ma So"].encode(),clientAddress)
                s.sendto(i["Ten Dia Diem"].encode(),clientAddress)
                s.sendto(i["Toa Do"].encode(),clientAddress)
                s.sendto(i["Thong Tin"].encode(),clientAddress)

        elif msg.decode()=="one":
            #cho de nhan dia diem can kiem
            DiaDiemTimKiem,clientAddress=s.recvfrom(2048)
            j=0 
            MaSo=""
            TenDiaDiem=""
            ToaDo=""
            ThongTin=""
            # bien kiem tra xem no co hay khong
            flag=0
            for i in location:
                if i["Ten Dia Diem"]==DiaDiemTimKiem.decode():
                    s.sendto(i["Ma So"].encode(),clientAddress)
                    s.sendto(i["Ten Dia Diem"].encode(),clientAddress)
                    s.sendto(i["Toa Do"].encode(),clientAddress)
                    s.sendto(i["Thong Tin"].encode(),clientAddress)
                    imageLink = "./Pictures/" + i["Ma So"] + ".png";
                    if (os.path.exists(imageLink) == False):
                      Gui_Anh_Client("./Pictures/default.png", clientAddress)
                    else:
                      Gui_Anh_Client(imageLink, clientAddress)  
                    flag=1  
                    
                    break
            #nếu khong co thi gui thong tin gia
            if flag==0:
                s.sendto(MaSo.encode(),clientAddress)
                s.sendto(TenDiaDiem.encode(),clientAddress)
                s.sendto(ToaDo.encode(),clientAddress)
                s.sendto(ThongTin.encode(),clientAddress)
            
            #Nếu nhan tin nhan là x ben client la dung 
        elif msg.decode()=='x':
            break

# Thread man hinh chinh cua server
def Main():
    #Window
    window = tk.Tk()
    window.geometry("800x600")
    window.resizable(width = False, height = False)
    window.title("SERVER")

    WindowLogin = tk.Frame(window, highlightthickness=3)
    def login():
        Main_Screen()
    
    DangNhapBtn = tk.Button(text="ĐĂNG NHẬP",height=5,width=15,command=login,bg="light yellow",justify = CENTER,fg = "red")
    DangNhapBtn.pack(expand=True)
    DangNhapBtn.place(x = 350, y = 200)

    WindowMainScreen = tk.Frame(window)
    
    def Main_Screen():
        WindowMainScreen.pack(side = "top", fill = "both", expand=True)
        WindowLogin.forget()
        HandleThread = threading.Thread(target=Client_Thread)
        HandleThread.start()



    TieuDe = tk.Label(WindowMainScreen, text="WELLCOME ", font="VNI-Dom 38",fg = "#03aaf9")
    TieuDe1 = tk.Label(WindowMainScreen, text="TO ", font="VNI-Dom 28",fg = "violet")
    TieuDe2 = tk.Label(WindowMainScreen, text="SERVER ", font="VNI-Dom 30",fg = "#1bc9b6")
    TieuDe3 = tk.Label(WindowMainScreen, text="NHOM 2", font="VNI-Dom 20",fg = "#f44336")
    TieuDe5 = tk.Label(WindowMainScreen, text="Phan Minh Xuan-20127395", font="VNI-Dom 16",fg = "#5bbb74")
    TieuDe6 = tk.Label(WindowMainScreen, text="Bui Duy Bao-20127444", font="VNI-Dom 16",fg = "#6fa8dc")
    TieuDe7 = tk.Label(WindowMainScreen, text="Nguyen Thai Bao-20127448", font="VNI-Dom 16",fg = "#FAB666")
    TieuDe8 = tk.Label(WindowMainScreen, text="Da Ket Noi!!!", font="VNI-Dom 16",fg = "red")
   

    TieuDe.pack()
    TieuDe.place(x = 260, y = 120)
    TieuDe1.pack()
    TieuDe1.place(x =375, y = 190)
    TieuDe2.pack()
    TieuDe2.place(x = 320, y = 240)
    TieuDe3.pack()
    TieuDe3.place(x =350, y = 360)
    TieuDe5.pack()
    TieuDe5.place(x = 285, y = 400)
    TieuDe6.pack()
    TieuDe6.place(x = 285, y = 440)
    TieuDe7.pack()
    TieuDe7.place(x = 285, y = 480)
    TieuDe8.pack()
    TieuDe8.place(x = 340, y = 50)
   
    window.mainloop()
  
main = threading.Thread(target=Main)
main.start()
    #-----------------------------------------------------