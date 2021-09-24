from SubWindows.BikeRoadClass import BikeRoadClass
from SubWindows.BikeStorageClass import *
from SubWindows.BikeLendingClass import *

class MainWindow:
    def __init__(self):
        global g_Tk
        g_Tk.title("Bike Appication")
        g_Tk.resizable(False, False)
        g_Tk.geometry("1024x768+300+0")

        self.canvas = Canvas(g_Tk).pack()

        #타이틀 라벨
        titleLabel = Label(g_Tk, relief = "ridge", borderwidth = 5, padx = 5, pady = 10, text = "수도권 자전거 정보 알리미", font = g_FontTitle)
        titleLabel.place(x = 15, y = 15)

        #페이지
        notebook = tkinter.ttk.Notebook(g_Tk, width= 1000, height= 620)
        notebook.place( x = 15, y = 100)

        #보관소
        self.bikeStorageFrame = Frame(g_Tk, relief = "ridge", borderwidth = 5)
        notebook.add(self.bikeStorageFrame, text = "보관소 정보")
        BikeStorageClass(self.bikeStorageFrame, "TempURL", 1)

        #자전거 도로
        self.bikeRoadFrame = Frame(g_Tk, relief = "ridge", borderwidth = 5)
        notebook.add(self.bikeRoadFrame, text="자전거 사고 다발지 정보")
        BikeRoadClass(self.bikeRoadFrame, "temp", 1)

        #대여소
        self.bikeRentalFrame = Frame(g_Tk, relief="ridge", borderwidth=5)
        notebook.add(self.bikeRentalFrame, text="공공 자전거 대여 정보")
        BikeLendingClass(self.bikeRentalFrame, "temp", 1)

        bikeIcon = Label(g_Tk, width = 125, height = 110)
        p = PhotoImage(file = "Bike.png")
        bikeIcon.configure(image = p)
        bikeIcon.image = p
        bikeIcon.place(x = 850, y = 5)

        g_Tk.mainloop()


MainWindow()

