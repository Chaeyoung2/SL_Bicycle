#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
from datetime import date, datetime, timedelta
import traceback

key = 'd9db836a29484038b3e29d0306baedb7'
TOKEN = '1156316080:AAGBm4OfNWPJpbNWu5lwz1PKjbYcKr-MC80'
MAX_MSG_LENGTH = 300
baseurl = 'https://openapi.gg.go.kr/BICYCL?KEY='+key
bot = telepot.Bot(TOKEN)

#url 완성
#Item에 해당하는 항목에 대해서만 처리하며,
#각 아이템 안에서 <로 시작해서 >로 끝나는 부분을 정규식을 이용하여 선택한 다음
#|로 치환하고, |를 구분자로 split 하여 데이터를 정제한다.
#마지막으로 파싱된 부분을 적당한 문자열로 가공
def getData(loc_param):
    res_list = []
    url = baseurl + '&SIGUN_CD=' + loc_param
    res_body = urlopen(url).read()
    soup = BeautifulSoup(res_body, 'html.parser')
    rows = soup.findAll('row')
    for item in rows:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[0]
            #row = parsed[0] + '/' + parsed[2] + '/' + parsed[6] + '/' + parsed[8] + '/공기주입기 배치:' + parsed[11] + '/전화번호:' + parsed[14]
        except IndexError:
            row = item.replace('|', ',')
        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
