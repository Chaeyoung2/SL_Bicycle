from tkinter import *
import tkinter.ttk
from tkinter import font
import json
import hashlib
import hmac
import base64
import urllib.parse as urlparse
import folium
import webbrowser

import googlemaps
import http.client

import smtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


host = "smtp.gmail.com"
port = "587"
htmlFileName = "logo.html"

msg = MIMEBase("multipart", "alternative")
msg['Subject'] = "자전거 보관소 프로필"
msg['From'] = "hepark8757@gmail.com"
msg['To'] = "haeun8731@naver.com"

from functools import partial

HEIGHT = 600
WIDTH  = 800

googleMapKey = "AIzaSyA2xxrhE8Yu226ZYUfaBxLrIGYkpnAfJmA"
googleMapURL = "https://maps.googleapis.com/maps/api/staticmap?"
#googleMap = googlemaps.Client(key = googleMapKey)
iconURL = "http://cdn.icon-icons.com/icons2/2035/PNG/512/weather_warning_signal_alert_exclamation_icon_124159.png"
g_Tk = Tk()
g_Font = font.Font(g_Tk, size=10, weight='bold', family = 'Consolas')
g_FontTitle = font.Font(g_Tk, size=16, weight='bold', family = "맑은 고딕")
g_FontSearch = font.Font(g_Tk, size=16, weight='normal', family = "맑은 고딕")
g_Font2 = font.Font(g_Tk, size=12, weight='bold', family = "맑은 고딕")

s = tkinter.ttk.Style()
s.configure('TNotebook.Tab', font=('URW Gothic L','11','bold'), background  = "black")

sigunguDict = {'가평군': 41820, '고양시': 41280, '과천시': 41290, '광명시': 41210, \
                    '광주시': 41610, '구리시': 41310, '군포시': 41410, '김포시': 41570, \
                    '남양주시': 41360, '동두천시': 41250, '부천시': 41190, '성남시': 41130, \
                    '수원시': 41110, '시흥시': 41390, '안산시': 41270, '안성시': 41550, \
                    '안양시': 41170, '양주시': 41630, '양평군': 41830, '여주시': 41670, \
                    '연천군': 41800, '오산시': 41370, '용인시': 41460, '의왕시': 41430, \
                    '의정부시': 41150, '이천시': 41500, '파주시': 41480, '평택시': 41220, \
                    '포천시': 41650, '하남시': 41450, '화성시': 41590 }