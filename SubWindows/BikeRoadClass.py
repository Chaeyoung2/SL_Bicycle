from SubWindows.SearchBaseClass import *
import chardet
import requests
import spam
from urllib import parse


class BikeRoadClass(SearchBaseClass):
    def __init__(self, frame, url, type):
        super().__init__(frame, url, type)
        self.apiKey = "/Tbbcycltfcacdarm?KEY=de8755ce9e9941a9a06e9569fe8c3578"
        self.zoomLevel = 11
        self.Label.configure(text = "출발 역")
        self.Label.place(x=40, y=20)
        self.Label2.configure(text = "도착 역")
        self.resultBox.destroy()
        self.sigunguBox.destroy()

        self.Label3 = tkinter.Label(frame, text="출발지부터 도착지까지의 경로를 출력하며, 주변의 사고다발지를 맵에 띄웁니다.", font=g_Font2, border=6,
                                     relief='ridge')
        self.Label3.place(x=40, y=90)

        self.StartPoint = ""
        self.EndPoint = ""

        self.startEntry = Entry(frame, font=g_Font2, width=9, border=2)
        self.startEntry.place(x=40, y=50)

        self.server = http.client.HTTPSConnection("openapi.gg.go.kr") # 서버를 연결시켜놓는다.

        self.mapLabel = Label(frame, padx=320, pady=210, bg="white",border=6,
                                     relief='ridge')
        self.mapLabel.place(x=40, y=130)

        self.chartButton = Button(frame, font=g_Font2, height=3, text="경기도 내 사고다발지 현황 차트", command=self.showChart)
        self.chartButton.place(x=720, y=300)

        self.zoomInButton = Button(frame, font=g_Font2, width = 3, height=3, text="+", command=self.zoomInImage)
        self.zoomInButton.place(x=700, y=500)

        self.zoomOutButton = Button(frame, font=g_Font2, width = 3, height=3, text="-", command=self.zoomOutImage)
        self.zoomOutButton.place(x=740, y=500)

    def zoomOutImage(self):
        self.zoomLevel -= 1

        tempURL = self.FinalImageURL
        tempURL += "&zoom=" + str(self.zoomLevel)
        tempURL = tempURL + "&key=" + googleMapKey

        r = requests.get(tempURL)
        p = PhotoImage(data=r.content)
        self.mapLabel.configure(image=p)
        self.mapLabel.image = p

    def zoomInImage(self):
        self.zoomLevel += 1

        tempURL = self.FinalImageURL
        tempURL += "&zoom=" + str(self.zoomLevel)
        tempURL = tempURL + "&key=" + googleMapKey

        r = requests.get(tempURL)
        p = PhotoImage(data=r.content)
        self.mapLabel.configure(image=p)
        self.mapLabel.image = p

    def showProfile(self, evt):

       pass

    def showChart(self):
        self.childTk = Tk()
        self.childTk.title("Bike Accident Ratio Chart")
        self.childTk.resizable(False, False)
        self.childTk.geometry("1200x700+300+10")
        self.sigunChartDict = {}
        self.isSorted = False
        if self.currentTree:
            rowElements = self.currentTree.getiterator("row")
            for row in rowElements:
                curSigunCode = row.find("SIGUN_NM").text
                if curSigunCode in self.sigunChartDict:
                    self.sigunChartDict[curSigunCode] = self.sigunChartDict[curSigunCode] + 1
                else:
                    self.sigunChartDict[curSigunCode] = 1

        self.canvas = Canvas(self.childTk, width=1200, height=700, bg='white')
        self.canvas.pack()
        x = 85
        cnt = 0
        prevY = 0
        self.sortButton = Button(self.childTk, text = "비율 구하기 : (C++연동)", command = self.sortByC)
        self.sortButton.place(x = 500, y = 670)

        self.realSortButton = Button(self.childTk, text="정렬하기", command=self.chartSort)
        self.realSortButton.place(x=700, y=670)

        for key, val in self.sigunChartDict.items():
            self.canvas.create_rectangle(x , 650-val*7,
                                         x+15, 650, fill = 'red', tags = 'temp')
            if (cnt != 0 and cnt != self.sigunChartDict.__len__()):
                self.canvas.create_line(x - 33, prevY-5, x + 7, 645 - val * 7, tags = 'temp')

            self.canvas.create_oval(x + 2, 650 - val * 7 - 10, x + 12, 650 - val * 7, fill='white', tags = 'temp')


            text = key
            text = text[:-1]
            self.canvas.create_text(x+7 , 660 ,text = text, tags = 'temp')
            x += 40
            prevY = 650-val*7
            cnt += 1

        pass

    def sortByC(self):
        x = 85
        self.canvas.delete("%")

        if self.isSorted:
            for key, val in self.sortedChart:
                self.canvas.create_text(x + 7, 675, text=str(round(spam.Divide(524, val), 2) * 100) + "%", tags="%")
                x += 40
        else:
            for key, val in self.sigunChartDict.items():
                self.canvas.create_text(x + 7, 675, text=str(round(spam.Divide(524, val), 2) * 100) + "%", tags = "%")
                x += 40

        pass

    def f2(self, x):
        return x[1]

    def chartSort(self):
        self.canvas.delete("%")
        self.canvas.delete('temp')
        self.sortedChart = sorted(self.sigunChartDict.items(), key = self.f2)
        self.isSorted = True

        x = 85
        cnt = 0
        prevY = 0


        for key, val in self.sortedChart:
            self.canvas.create_rectangle(x , 650-val*7,
                                         x+15, 650, fill = 'red', tags = 'temp')
            if (cnt != 0 and self.sortedChart.__len__()):
                self.canvas.create_line(x - 33, prevY-5, x + 7, 645 - val * 7, tags = 'temp')

            self.canvas.create_oval(x + 2, 650 - val * 7 - 10, x + 12, 650 - val * 7, fill='white', tags = 'temp')


            text = key
            text = text[:-1]
            self.canvas.create_text(x+7 , 660 ,text = text, tags = 'temp')
            x += 40
            prevY = 650-val*7
            cnt += 1

    def search(self):
        self.startPoints = []
        self.endPoints = []
        for i in range(2):
            address = ""
            if i==0:
                address = self.startEntry.get()
            else:
                address = self.entry.get()
            address = parse.quote(address)
            geocodeURL = "/maps/api/geocode/xml?address=" + address + "&language=ko&key=" + googleMapKey
            # http.client.HTTPSConnection("openapi.gg.go.kr")
            # self.apiKey = "/BICYCLDEPOSIT?KEY=837c6677d0794a89bb57ca8a0c6dd523"
            googleServer = http.client.HTTPSConnection("maps.googleapis.com")
            googleServer.request("GET", geocodeURL, None)
            r = googleServer.getresponse()
            if r.status == 200:
                reqBody = r.read()
                encodingType = chardet.detect(reqBody)  # 인코딩타입을 알아온다.
                finalreqBody = reqBody.decode(encodingType.__getitem__('encoding'))  # 디코딩을 진행한다.
                tree = ElementTree.fromstring(finalreqBody)  # 디코딩된 데이터를 ElementTree로 저장->Tree순회하면서 데이터 탐색 가능.

                geomtetries = tree.getiterator("geometry")  # geoccode xml파일은 각 Element의 위도,경도를 geometry라는 이름으로 지정해놓았음.
                for geometry in geomtetries:
                    location = tree.getiterator("location")
                    isFind = False
                    for loc in location:
                        if i==0:
                            self.StartPoint = loc.find("lat").text+ "," + loc.find("lng").text
                            self.startPoints.append(float(loc.find("lat").text))
                            self.startPoints.append(float(loc.find("lng").text))

                        else:
                            self.EndPoint = loc.find("lat").text+ "," + loc.find("lng").text
                            self.endPoints.append(float(loc.find("lat").text))
                            self.endPoints.append(float(loc.find("lng").text))

                        isFind = True
                        break
                    if isFind:
                        break

        # 이제 시작 , 끝좌표를 아니 지도를 그릴 때
        googleServer = http.client.HTTPSConnection("maps.googleapis.com")
        directionURL = "/maps/api/directions/xml?origin=" + self.StartPoint + "&destination=" + self.EndPoint + "&mode=transit&departure_time=now&key=" + googleMapKey
        googleServer.request("GET", directionURL, None)
        r = googleServer.getresponse()
        polylineText = ""
        if r.status == 200:
            reqBody = r.read()
            encodingType = chardet.detect(reqBody)  # 인코딩타입을 알아온다.
            finalreqBody = reqBody.decode(encodingType.__getitem__('encoding'))  # 디코딩을 진행한다.
            tree = ElementTree.fromstring(finalreqBody)  # 디코딩된 데이터를 ElementTree로 저장->Tree순회하면서 데이터 탐색 가능.
            overview_polylines = tree.getiterator("overview_polyline")  # directions xml파일의 polyline을 갖고온다.
            bounds = tree.getiterator("bounds")  # directions xml파일의 polyline을 갖고온다.
            self.bounds = []
            for bound in bounds:
                southwest = bound.getiterator("southwest")
                for loc in southwest:
                    self.bounds.append(float(loc.find("lat").text))
                    self.bounds.append(float(loc.find("lng").text))
                    break

                northeast = bound.getiterator("northeast")
                for loc in northeast:
                    self.bounds.append(float(loc.find("lat").text))
                    self.bounds.append(float(loc.find("lng").text))
                    break
                break

            for polyline in overview_polylines:
                polylineText = polyline.find("points").text
                break

        self.server.request("GET", "/Tbbcycltfcacdarm?&pSize=1000&pIndex=1&KEY=de8755ce9e9941a9a06e9569fe8c3578", None)

        self.req = self.server.getresponse()
        if self.req.status == 200:
            reqBody = self.req.read()
            encodingType = chardet.detect(reqBody)  # 인코딩타입을 알아온다.
            finalreqBody = reqBody.decode(encodingType.__getitem__('encoding'))  # 디코딩을 진행한다.
            tree = ElementTree.fromstring(finalreqBody)  # 디코딩된 데이터를 ElementTree로 저장->Tree순회하면서 데이터 탐색 가능.

            rowElements = tree.getiterator("row")  # 도로보관소 xml파일은 각 Element를 row라는 이름으로 지정해놓았음.
            self.currentTree = tree

            warningTexts = []

            for row in rowElements:
                curLat = row.find("LAT").text
                curLogt = row.find("LOGT").text
                curLatf = float(curLat)
                curLogtf = float(curLogt)
                if curLatf >= self.bounds[0] and curLatf <=self.bounds[2] and curLogtf >= self.bounds[1] and curLogtf <= self.bounds[3]\
                        and warningTexts.__len__() <= 175:
                    warningTexts.append("&markers=size:tiny%7Ccolor:red%7Clabel:W%7C"+curLat+","+curLogt)

                #("&markers=anchor:topleft%7Cicon:"+parse.quote(iconURL)+row.find("LOGT").text+","+row.find("LAT").text)

            #최종적으로 그림을 그린다.
            finalImageURL = "https://maps.googleapis.com/maps/api/staticmap?&size=1000x450&maptype=roadmap&path=weight:8%7Ccolor:Black%7Cenc:"+\
                            polylineText + "&markers=color:blue%7Clabel:S%7C" + self.StartPoint + "&markers=color:orange%7Clabel:E%7C" + self.EndPoint
            centerText = "&center=" + str((self.bounds[0] + self.bounds[2]) / 2.0) + "," + str(
                (self.bounds[1] + self.bounds[3]) / 2.0)

            finalImageURL += centerText
            for warningText in warningTexts:
                finalImageURL = finalImageURL+ warningText
            self.FinalImageURL = finalImageURL
            finalImageURL += "&zoom="+str(self.zoomLevel)
            finalImageURL = finalImageURL + "&key=" + googleMapKey


            r = requests.get(finalImageURL)

            p = PhotoImage(data=r.content)
            self.mapLabel.configure(image=p)
            self.mapLabel.image = p



