import tkinter as tk
import socket
from tkinter import *
import tkinter
import threading
from tkinter import messagebox
HOST="127.0.0.1"
SERVER_PORT=65432
FORMAT="utf8"

MaSo = ""
TenDiaDiem = ""
ToaDo = ""
ThongTin = ""

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.connect((HOST,SERVER_PORT))


# Khai bao man hinh giao dien GUI - tkinner
window = tk.Tk()
window.geometry("1000x500")
window.resizable(width = False, height = False)
window.title("Travel App")


# Frame man hinh 1 va man hinh 2
ManHinh1 = tk.Frame(window, width = 1000, height = 500, highlightbackground="#2faf49", highlightthickness=3)
ManHinh2 = tk.Frame(window, width = 1000, height = 500, highlightbackground="#1bc9b6", highlightthickness=3)
ManHinh1.pack()
ManHinh1.place(x = 0, y = 0)

# Ham chuyen tư man hinh 2 sang man hinh 1
def Quay_Lai_Man_Hinh():
    ManHinh2.forget()
    ManHinh1.pack()

# Ham chuyen sang man hinh 2
def Chuyen_Man_Hinh():
    ManHinh1.forget()
    ManHinh2.pack()
    
# Ham nhan image tu server    
def Nhan_Anh_Tu_Server(imageID):
    file = open(imageID + ".png", "wb")
    while True:
        Anh = client.recv(2048)
        if not Anh:
            break
        file.write(Anh)
    file.close()

# Ham phong to image
def Phong_To_Anh():
    global photoLink
    global img2

    NewWindow = Toplevel(window)
    NewWindow.title(photoLink)
    NewWindow.geometry("1500x900")
    canvas = Canvas(NewWindow, width=1500, height=900)
    canvas.pack(expand = YES)

    img2 = tk.PhotoImage(file = photoLink)
    img2 = img2.zoom(2)
    canvas.create_image(750,450,image = img2)


#Ham nhan va xu li khi nhan tat ca thong tin cac dia diem tu server
def Danh_Sach_Dia_Diem():
    
    location = []
    msg = "full"
    client.sendto(msg.encode(),(HOST,SERVER_PORT))

    global MaSo
    global TenDiaDiem
    global ToaDo
    global ThongTin


    
    message,serverAddress=client.recvfrom(2048)
    NoLocation=int(message.decode())


        

    for i in range(0, NoLocation):
        message,serverAddress=client.recvfrom(2048)
        MaSo=message.decode()
        message,serverAddress=client.recvfrom(2048)
        TenDiaDiem=message.decode()
        message,serverAddress=client.recvfrom(2048)
        ToaDo=message.decode()
        message,serverAddress=client.recvfrom(2048)
        ThongTin=message.decode()
        location.append({ "Ma So":MaSo, "Ten Dia Diem":TenDiaDiem , "Toa Do":ToaDo , "Thong Tin":ThongTin})
    
    for i in location:
        ThongTinDanhSachDiaDiem.insert('end', "  Ma So: ")
        ThongTinDanhSachDiaDiem.insert('end', i['Ma So'])
        ThongTinDanhSachDiaDiem.insert('end', "\n")
        
        ThongTinDanhSachDiaDiem.insert('end', "  Ten Dia Diem: ")
        ThongTinDanhSachDiaDiem.insert('end', i['Ten Dia Diem'])
        ThongTinDanhSachDiaDiem.insert('end', "\n")
        
        ThongTinDanhSachDiaDiem.insert('end', "  Toa Do: ")
        ThongTinDanhSachDiaDiem.insert('end', i['Toa Do'])
        ThongTinDanhSachDiaDiem.insert('end', "\n")
        
        ThongTinDanhSachDiaDiem.insert('end', "  Thong Tin: ")
        ThongTinDanhSachDiaDiem.insert('end', i['Thong Tin'])
        ThongTinDanhSachDiaDiem.insert('end', "\n")
        ThongTinDanhSachDiaDiem.insert('end', "\n")

        
       
    ThongTinDanhSachDiaDiemFrame.pack()
    ThongTinDanhSachDiaDiemFrame.place(x = 260, y = 100)
    ThongTinDanhSachDiaDiem.pack()
    ThongTinDanhSachDiaDiem.place(x = 0, y = 0)
    ThongTinDanhSachDiaDiem.configure(state = 'disabled')
    #Chuyen_Man_Hinh()
        

    

#Xuat cac thong tin cua screen 1 ve xuat tat ca dia diem

XuatDiaDiemBtn = tk.Button(ManHinh1, text="Danh Sach Dia Diem", font="VNI-Dom 10", fg = "red",bg="light yellow", command=Danh_Sach_Dia_Diem)
XuatDiaDiemBtn.pack()
XuatDiaDiemBtn.place(x = 450, y = 360)


#Ham yeu cau va nhan tim kiem mot dia diem tu server
def Tim_Mot_Dia_Diem():
    location=[]   
    #Gui yeu cau muon tim kiem mot dia diem
    msg = "one"
    client.sendto(msg.encode(),(HOST,SERVER_PORT))
    if msg=="one":
        #Nhap ten dia diem muon kiem
        DiaDiemTimKiem = DiaDiem.get()
        client.sendto(DiaDiemTimKiem.encode(),(HOST,SERVER_PORT))
        
        global MaSo
        global TenDiaDiem
        global ToaDo
        global ThongTin

        message,serverAddress=client.recvfrom(2048)
        MaSo=message.decode()
        message,serverAddress=client.recvfrom(2048)
        TenDiaDiem=message.decode()
        message,serverAddress=client.recvfrom(2048)
        ToaDo=message.decode()
        message,serverAddress=client.recvfrom(2048)
        ThongTin=message.decode()
        location.append({ "Ma So":MaSo, "Ten Dia Diem":TenDiaDiem , "Toa Do":ToaDo , "Thong Tin":ThongTin}) 
        if MaSo == "":
            print("Khong Tim Thay")
        elif MaSo!="":
            Nhan_Anh_Tu_Server(MaSo)

#Image phai de la bien global de khong bug
photoLink = ""
img = tk.PhotoImage() 
img2 = tk.PhotoImage()

# Ham xuat ra man hinh 2 dia diem da nhan tu server
def Xuat_Dia_Diem():
    Tim_Mot_Dia_Diem() #Nhan cac dia diem

    MaSoCuaDiaDiem = tk.Label(ManHinh2, text = "MA SO: ", font="VNI-Dom 10",fg = "green")
    MaSoCuaDiaDiemText = tk.Label(ManHinh2, text = MaSo, font="  VNI-Dom 14",fg = "#c74b4b")

    TenCuaDiaDiem = tk.Label(ManHinh2, text = "TEN DIA DIEM: ", font="VNI-Dom 10",fg = "green")
    TenCuaDiaDiemText = tk.Label(ManHinh2, text =   TenDiaDiem, font="  VNI-Dom 15",fg = "#c74b4b")

    ToaDoCuaDiaDiem = tk.Label(ManHinh2, text = "TOA DO: ", font="VNI-Dom 10",fg = "green")
    ToaDoCuaDiaDiemText = tk.Label(ManHinh2, text = ToaDo, font="  VNI-Dom 14",fg = "#c74b4b")

    ThongTinTextFrame = tk.Frame(ManHinh2, width=420, height=170)
    ThongTinTextFrame.pack_propagate(0) 
    
    global photoLink
    photoLink = MaSo + ".png"

    global img
    img = tk.PhotoImage(file=photoLink) #Image phai de la bien global
    
    #Xuat hinh anh trong frame
    XuatHinhAnhBtn = tk.Button(ManHinh2, image=img, width= 480, height=433, borderwidth=0, command=Phong_To_Anh)
    XuatHinhAnhBtn.pack()
    XuatHinhAnhBtn.place(x=500, y= 0) 

    ThongTinCuaDiaDiem = tk.Label(ManHinh2, text = "THONG TIN: ", font="VNI-Dom 10",fg = "green")
    ThongTinCuaDiaDiemText = tk.Text(ThongTinTextFrame, width = 50, height= 10, wrap='word',fg = "#c74b4b")
    ThongTinCuaDiaDiemText.insert('end', ThongTin)
    ScroballText = Scrollbar(ThongTinTextFrame)
    ScroballText.pack(side=RIGHT, fill=BOTH)
    ThongTinCuaDiaDiemText.config(yscrollcommand=ScroballText.set)
    ScroballText.config(command=ThongTinCuaDiaDiemText.yview)

    MaSoCuaDiaDiem.pack()
    MaSoCuaDiaDiem.place(x = 10, y = 10)
    MaSoCuaDiaDiemText.pack()
    MaSoCuaDiaDiemText.place(x = 120,y = 10)
    TenCuaDiaDiem.pack()
    TenCuaDiaDiem.place(x = 10,y = 50)
    TenCuaDiaDiemText.pack()
    TenCuaDiaDiemText.place(x = 120, y= 50)
    ToaDoCuaDiaDiem.pack()
    ToaDoCuaDiaDiem.place(x = 10, y = 90)
    ToaDoCuaDiaDiemText.pack()
    ToaDoCuaDiaDiemText.place(x = 120, y = 90)
    ThongTinCuaDiaDiem.pack()
    ThongTinCuaDiaDiem.place(x = 10 , y = 130)
    ThongTinTextFrame.pack()
    ThongTinTextFrame.place(x = 10 , y = 180)
    ThongTinCuaDiaDiemText.pack()
    ThongTinCuaDiaDiemText.place(x = 0, y = 0)
    ThongTinCuaDiaDiemText.configure(state='disabled')
    
    #Neu nhu tim thay dia diem, chuyen qua screen 2
    if (MaSo != ""):
        Chuyen_Man_Hinh()
    
    #Ham xoa thong tin screen 2 de nhan thong tin moi
    def Xoa_Thong_Tin():
        MaSoCuaDiaDiemText.place_forget()
        TenCuaDiaDiemText.place_forget()
        ToaDoCuaDiaDiemText.place_forget()
        
    TroLai = tk.Button(ManHinh2, text ="Tro Lai", font="VNI-Dom 12", fg = "blue",bg="light yellow", command=lambda:[Quay_Lai_Man_Hinh(),Xoa_Thong_Tin()])
    TroLai.pack()
    TroLai.place(x = 10 , y = 410)

    def msgbox():
        messagebox.showinfo("NOTICE","ĐÃ TẢI THÀNH CÔNG")
    
    ButtonX = tk.Button(ManHinh2,text="TẢI ẢNH",font="VNI-Dom 12", fg = "blue",bg="light yellow",command= msgbox)

    ButtonX.pack()
    ButtonX.place(x=700,y=440)

# Xuat cac thanh phan cua screen 1 
DiaDiemLabel = tk.Label(ManHinh1, text = " NHAP MOT DIA DIEM: ", font="VNI-Dom 12",fg = "blue")
DiaDiem = tk.Entry(ManHinh1, highlightthickness=2, highlightcolor="blue", font="VNI-Dom 10",bg="light yellow")
DiaDiemBtn = tk.Button(ManHinh1, text="Tim Kiem", font="VNI-Dom 10", fg = "red", command=Xuat_Dia_Diem,bg="light yellow")

DiaDiem.pack()
DiaDiem.place(x = 450, y = 45)
DiaDiemLabel.pack()
DiaDiemLabel.place(x = 210 , y = 45)
DiaDiemBtn.pack()
DiaDiemBtn.place(x = 650, y = 43)

TieuDe = tk.Label(ManHinh1, text="WELLCOME ", font="VNI-Dom 38",fg = "#03aaf9")
TieuDe1 = tk.Label(ManHinh1, text="TO ", font="VNI-Dom 28",fg = "violet")
TieuDe2 = tk.Label(ManHinh1, text="TRAVEL-APP ", font="VNI-Dom 30",fg = "#1bc9b6")
TieuDe3 = tk.Label(ManHinh1, text="MANG MAY TINH", font="VNI-Dom 20",fg = "#1bc9b6")
TieuDe4 = tk.Label(ManHinh1, text="20CLC01", font="VNI-Dom 18",fg = "#509ed8")
TieuDe5 = tk.Label(ManHinh1, text="Do An", font="VNI-Dom 22",fg = "#017075")
TieuDe6 = tk.Label(ManHinh1, text="DIA", font="VNI-Dom 25",fg = "#CC0080")
TieuDe7 = tk.Label(ManHinh1, text="DIEM", font="VNI-Dom 25",fg = "#FAB666")
TieuDe8 = tk.Label(ManHinh1, text="YEU", font="VNI-Dom 25",fg = "#1bc9b6")
TieuDe9 = tk.Label(ManHinh1, text="THICH", font="VNI-Dom 25",fg = "#00CC1A")


TieuDe.pack()
TieuDe.place(x = 370, y = 120)
TieuDe1.pack()
TieuDe1.place(x =480, y = 190)
TieuDe2.pack()
TieuDe2.place(x = 400, y = 240)
TieuDe3.pack()
TieuDe3.place(x =20, y = 150)
TieuDe4.pack()
TieuDe4.place(x = 80, y = 210)
TieuDe5.pack()
TieuDe5.place(x = 800, y = 100)
TieuDe6.pack()
TieuDe6.place(x = 780, y = 140)
TieuDe7.pack()
TieuDe7.place(x = 810, y = 180)
TieuDe8.pack()
TieuDe8.place(x = 840, y = 220)
TieuDe9.pack()
TieuDe9.place(x = 870, y = 260)

ManHinh1.pack_propagate(0)
ManHinh2.pack_propagate(0)

ThongTinDanhSachDiaDiemFrame = tk.Frame(ManHinh1, width=500, height=230)
ThongTinDanhSachDiaDiemFrame.pack_propagate(0)
ThongTinDanhSachDiaDiem = tk.Text(ThongTinDanhSachDiaDiemFrame, width = 60, height=14, wrap='word')
ScroballText = Scrollbar(ThongTinDanhSachDiaDiemFrame)
ScroballText.pack(side=RIGHT, fill=BOTH)
ThongTinDanhSachDiaDiem.config(yscrollcommand=ScroballText.set)
ScroballText.config(command=ThongTinDanhSachDiaDiem.yview)



window.mainloop()
client.close()