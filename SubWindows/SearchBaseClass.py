from Globals import *
from xml.etree import ElementTree

class SearchBaseClass:
    def search(self):
        pass

    def __init__(self, frame, url, type):
        self.apiKey = ''
        self.frame = frame

        if type == 0:
            self.Label = tkinter.Label(frame, text="시/군/구", font=g_Font)
            self.Label.place(x=21, y=10)

            self.Label2 = tkinter.Label(frame, text="동/읍/면", font=g_Font)
            self.Label2.place(x=135, y=10)

            self.sigunguBox = tkinter.ttk.Combobox(frame, font=g_Font, width=12, height=1)
            self.sigunguBox.place(x=21, y=30)

            self.entry = Entry(frame, font=g_Font, width=9, border=2)
            self.entry.place(x=135, y=30)

            self.searchButton = Button(frame, font=g_Font, text="검색", command=self.search)
            self.searchButton.place(x=200, y=27)

            self.resultBox = Listbox(frame, font=g_Font, activestyle='none', width=40, height=22, border=6,
                                     relief='ridge' \
                                     )
            self.resultBox.place(x=20, y=60)

        elif type == 1:
            self.Label = tkinter.Label(frame, text="시군명", font=g_Font2)
            self.Label.place(x=20, y=20)

            self.Label2 = tkinter.Label(frame, text="시군 코드", font=g_Font2)
            self.Label2.place(x=160, y=20)

            self.sigunguBox = tkinter.ttk.Combobox(frame, font=g_Font2, width=12, height=1)
            self.sigunguBox.place(x=20, y=50)

            self.entry = Entry(frame, font=g_Font2, width=9, border=2)
            self.entry.place(x=160, y=50)

            self.searchButton = Button(frame, font=g_Font2, width = 4, height = 1, text="검색", command=self.search)
            self.searchButton.place(x=255, y=45)

            self.resultBox = Listbox(frame, font=g_Font2, activestyle='none', width=40, height=22, border=6,
                                     relief='ridge' \
                                     )
            self.resultBox.place(x=20, y=102)






