from SubWindows.SearchBaseClass import *
import chardet
import requests
import folium
import webbrowser
# import PIL import Image
# import PIL import ImageTk #resize2
#import tkinter as tk
#from PIL import Image, ImageTk
#import io


class BikeLendingClass(SearchBaseClass):
    def __init__(self, frame, url, type):
        super().__init__(frame, url, type)
        self.apiKey = "/BICYCL?KEY=d9db836a29484038b3e29d0306baedb7"

        self.Label2.configure(text="동/읍/면")

        self.sigunguBox['values'] = ('수원시', '성남시', '용인시', '안양시', '안산시', '과천시', '광명시', '광주시',\
                                     '군포시', '부천시', '시흥시', '김포시', '안성시', '오산시', '의왕시', '이천시',\
                                     '평택시', '하남시', '화성시', '여주시', '양평군', '고양시', '구리시', '남양주시',\
                                     '동두천시', '양주시', '의정부시', '파주시', '포천시', '연천군', '가평군')
        self.sigunguBox['height'] = 10
        self.resultBox.bind('<<ListboxSelect>>', self.showProfile)
        self.currentResultBoxNum = 0 #search 할 때 사용

        self.server = http.client.HTTPSConnection("openapi.gg.go.kr")

        self.profileText = Label(frame, background="white", width=55, height=10, text="None", font=g_Font2,border=6,
                                     relief='ridge')
        self.profileText.place(x=420, y=90)

        self.mapLabel = Label(frame, padx=275, pady=130, bg="white",border=6,
                                     relief='ridge')
        self.mapLabel.place(x=420, y=320)


    def showProfile(self, evt):
        if self.currentTree:
            curSelection = list(self.resultBox.curselection())
            if (curSelection.__len__() > 0):
                index = int(curSelection[0])
                value = self.resultBox.get(index) #인덱스에 해당하는 값
                name = "<  " + value + "  >"
                for row in self.currentTree.getiterator("row"):
                    if row.find("BICYCL_LEND_PLC_NM_INST_NM").text == value:
                        telno = "[☎ Tel No.] " + row.find("MNGINST_TELNO").text
                        restday = "[휴무일] " + row.find("RESTDAY_INFO").text
                        charg = "[요금] " + row.find("BICYCL_UTLZ_CHRG_INFO").text
                        airinjek = "[공기 주입기 비치] " + row.find("AIR_INJEK_POSTNG_YN").text
                        addr1 = "[지번 주소] " + row.find("REFINE_LOTNO_ADDR").text
                        self.profileText["text"] = name + '\n' + telno + '\n' + restday + '\n' + charg + '\n' + addr1 + '\n' # 최종텍스트 출력
                        lat = row.find("REFINE_WGS84_LAT").text #위도
                        logt = row.find("REFINE_WGS84_LOGT").text #경도


                        #1. 구글api
                        r = requests.get("https://maps.googleapis.com/maps/api/staticmap?size=550x250&maptype=roadmap&\
                        zoom=15&markers=color:blue%7Clabel:S%7C" + lat + "," + logt + "&key=AIzaSyA2xxrhE8Yu226ZYUfaBxLrIGYkpnAfJmA")

                        #1.1 resize-1
                        p = PhotoImage(data=r.content)
                        #p.zoom(25)
                        #p.subsample(32)

                        #1.2 resize-2
                        #image.resize((50, 50), Image.ANTIALIAS)

                        #1.3 resize-3 #https://stackoverflow.com/questions/14759637/python-pil-bytes-to-image
                        # imageBinaryBytes = r.content #resize3
                        # imageStream = io.BytesIO(imageBinaryBytes)
                        # imageFile = Image.open(imageStream)
                        # #imageFile.size(320, 240)
                        #p = PhotoImage(imageFile)

                        self.mapLabel.configure(image=p)
                        self.mapLabel.image = p

                        #2. folium
                        # # 위도 경도 지정
                        # map_osm = folium.Map(location=[lat, logt], zoom_start=13)
                        # # 마커 지정
                        # folium.Marker([lat, logt], popup='한국산업기술대').add_to(map_osm)
                        # # html 파일로 저장
                        # map_osm.save('osm.html')
                        # webbrowser.open_new('osm.html')
                        # Button(window, text='folium 지도', command=Pressed).pack()

                        break
    def search(self):
        currentSigun = self.sigunguBox.get()
        currentDong = self.entry.get()
        currentSigunCD = sigunguDict.get(currentSigun)
        # 한 시/군의 설치수가 350개는 넘지 않을것같아 index1에 size 350값으로 질의
        self.server.request("GET", self.apiKey + "&pIndex=1" + "&pSize=350" + \
                            "&SIGUN_CD=" + str(currentSigunCD), None)

        self.req = self.server.getresponse()
        if self.req.status == 200:
            reqBody = self.req.read()
            encodingType = chardet.detect(reqBody)  # 인코딩타입을 알아온다.
            finalreqBody = reqBody.decode(encodingType.__getitem__('encoding'))  # 디코딩을 진행한다.
            tree = ElementTree.fromstring(finalreqBody)  # 디코딩된 데이터를 ElementTree로 저장->Tree순회하면서 데이터 탐색 가능.

            rowElements = tree.getiterator("row")  # 도로보관소 xml파일은 각 Element를 row라는 이름으로 지정해놓았음.
            insertIndex = 0
            self.resultBox.delete(0, self.currentResultBoxNum)

            if len(currentDong) == 0:  # 동을 입력하지 않았을때는 시/군 코드로 검색 후 바로 결과 출력
                for row in rowElements:
                    if row.find("SIGUN_CD").text == str(currentSigunCD):
                        self.resultBox.insert(insertIndex, row.find("BICYCL_LEND_PLC_NM_INST_NM").text)
                        insertIndex += 1

            else:  # 동을 입력했을 때는 시/군 코드 검색 결과중 동이 일치하는 것만 출력
                for row in rowElements:
                    if row.find("SIGUN_CD").text == str(currentSigunCD):
                        addr = row.find("REFINE_LOTNO_ADDR").text
                        if addr != None and addr.__contains__(currentDong):
                            self.resultBox.insert(insertIndex, row.find("BICYCL_LEND_PLC_NM_INST_NM").text)
                            insertIndex += 1

            self.currentTree = tree
            self.currentResultBoxNum = insertIndex





