from SubWindows.SearchBaseClass import *
import chardet
import requests



class BikeStorageClass(SearchBaseClass):
    def __init__(self, frame, url, type):
        super().__init__(frame, url, type)
        self.apiKey = "/BICYCLDEPOSIT?KEY=837c6677d0794a89bb57ca8a0c6dd523"

        self.Label2.configure(text = "동/읍/면")
        self.sigunguBox['values'] = ('수원시', '성남시', '용인시', '안양시', '안산시', '과천시', '광명시', '광주시',\
                                     '군포시', '부천시', '시흥시', '김포시', '안성시', '오산시', '의왕시', '이천시',\
                                     '평택시', '하남시', '화성시', '여주시', '양평군', '고양시', '구리시', '남양주시',\
                                     '동두천시', '양주시', '의정부시', '파주시', '포천시', '연천군', '가평군')

        self.sigunguBox['height'] = 10
        self.resultBox.bind('<<ListboxSelect>>', self.showProfile)

        self.currentResultBoxNum = 0

        self.server = http.client.HTTPSConnection("openapi.gg.go.kr") # 서버를 연결시켜놓는다.

        self.profileText = Label(frame, background="white", width=55, height=10, text="None", font=g_Font2,border=6,
                                     relief='ridge')
        self.profileText.place(x=420, y=90)

        self.mapLabel = Label(frame, padx=275, pady=130, bg="white",border=6,
                                     relief='ridge')
        self.mapLabel.place(x=420, y=320)

        self.sendMailButton = Button(frame, text = "보관소 정보 Gmail 보내기",font=g_Font2,border=6, command = self.sendMail)
        self.sendMailButton.place(x= 765, y = 30)
    def sendMail(self):
        imageFD = open("googleMap.png", 'rb')
        Image = MIMEImage(imageFD.read())
        Image.add_header('Content-Disposition', 'attachment', filename="지도.png")
        msg.attach(Image)
        imageFD.close()

        HtmlPart = MIMEText(self.profileText["text"], 'html', _charset='UTF-8')
        msg.attach(HtmlPart)

        s = smtplib.SMTP(host, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("hepark8757@gmail.com", "oebgitogi1")
        s.sendmail("hepark8757@gmail.com","haeun8731@naver.com",msg.as_string())
        s.close()

        pass
    def showProfile(self, evt):
        if self.currentTree:
            curSelection = list(self.resultBox.curselection())
            if(curSelection.__len__() > 0):
                index = int(curSelection[0])
                value = self.resultBox.get(index)
                name = "<  " + value + "  >"
                for row in self.currentTree.getiterator("row"):
                    if row.find("BICYCL_DEPOSIT_NM_TITLE").text == value:
                        telno = "[ ☎ Tel No. : " + row.find("MNGINST_TELNO").text + " ]"
                        addr1 = "지번 주소 : " + row.find("REFINE_LOTNO_ADDR").text
                        addr_road = row.find("REFINE_ROADNM_ADDR").text
                        if addr_road != None:
                            addr2 = "도로명 주소 : " + row.find("REFINE_ROADNM_ADDR").text
                        else:
                            addr2 = "도로명 주소 : 지원하지 않음"
                        self.profileText["text"] = name + '\n' + telno + '\n' + addr1 + '\n' + addr2 #최종텍스트 출력

                        lat = row.find("LAT").text
                        logt = row.find("LOGT").text

                        r = requests.get("https://maps.googleapis.com/maps/api/staticmap?size=550x250&maptype=roadmap&\
                        zoom=15&markers=color:blue%7Clabel:S%7C"+ lat + ","+logt+"&key=AIzaSyA2xxrhE8Yu226ZYUfaBxLrIGYkpnAfJmA")

                        imageFD = open("googleMap.png", 'wb')
                        imageFD.write(r.content)
                        imageFD.close()


                        p = PhotoImage(data = r.content)
                        self.mapLabel.configure(image = p)
                        self.mapLabel.image = p
                        self.ImageData = r.content
                        break


    def search(self):
        currentSigun = self.sigunguBox.get()
        currentDong = self.entry.get()
        currentSigunCD = sigunguDict.get(currentSigun)
        # 한 시/군의 설치수가 350개는 넘지 않을것같아 index1에 size 350값으로 질의
        self.server.request("GET", self.apiKey + "&pIndex=1" + "&pSize=350"+\
                            "&SIGUN_CD=" + str(currentSigunCD), None)

        self.req = self.server.getresponse()
        if self.req.status == 200:
            reqBody = self.req.read()
            encodingType = chardet.detect(reqBody)  # 인코딩타입을 알아온다.
            finalreqBody = reqBody.decode(encodingType.__getitem__('encoding'))  # 디코딩을 진행한다.
            tree = ElementTree.fromstring(finalreqBody)  #디코딩된 데이터를 ElementTree로 저장->Tree순회하면서 데이터 탐색 가능.

            rowElements = tree.getiterator("row")  # 도로보관소 xml파일은 각 Element를 row라는 이름으로 지정해놓았음.
            insertIndex = 0
            self.resultBox.delete(0, self.currentResultBoxNum)

            if len(currentDong) == 0:  # 동을 입력하지 않았을때는 시/군 코드로 검색 후 바로 결과 출력
                for row in rowElements:
                    if row.find("SIGUN_CD").text == str(currentSigunCD):
                        self.resultBox.insert(insertIndex, row.find("BICYCL_DEPOSIT_NM_TITLE").text)
                        insertIndex += 1

            else:  # 동을 입력했을 때는 시/군 코드 검색 결과중 동이 일치하는 것만 출력
                for row in rowElements:
                    if row.find("SIGUN_CD").text == str(currentSigunCD):
                        addr = row.find("REFINE_LOTNO_ADDR").text
                        if addr != None and addr.__contains__(currentDong):
                            self.resultBox.insert(insertIndex, row.find("BICYCL_DEPOSIT_NM_TITLE").text)
                            insertIndex += 1

            self.currentTree = tree
            self.currentResultBoxNum = insertIndex
