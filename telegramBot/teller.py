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

import noti


def replyAptData(user, loc_param='수원'):
    print(user, loc_param)
    res_list = noti.getData( loc_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.' )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

#텔레그렘으로 메시지(명령어)를 보낼 때마다 어떤 메시지가 들어왔는지
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '텍스트 이외의 메시지는 처리할 수 없습니다')
        return

    text = msg['text']
    args = text.split(' ')

    #args[1](법정동 코드)에 해당하는 2017년 5월 아파트 실거래가 자료를 xml parsing
    if text.startswith('거래') and len(args) > 1:
        print('try to 거래', args[1])
        replyAptData(args[1], chat_id, args[2])
    elif text.startswith('지역') and len(args)>1:
        print('try to 지역', args[1])
        replyAptData(chat_id, args[1] )
    elif text.startswith('시군코드') and len(args)>1:
        print('try to 시군코드', args[1])
        replyAptData(chat_id, args[1] )
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    else:
        noti.sendMessage(chat_id, """"모르는 명령어입니다.\n지역 [지역명] \n시군코드 [시군코드] 중 하나의 명령을 입력하세요.\n
        지역 ['수원시 41110', '성남시 41130', '용인시 41460', '안양시 41170', '안산시 41270', '과천시 41290', '광명시 41210', '광주시 41610',\
                                     '군포시 41410', '부천시 41190', '시흥시 41390', '김포시 41570', '안성시 41550', '오산시 41370', '의왕시 41430', '이천시 41500',\
                                     '평택시 41220', '하남시 41450', '화성시 41590', '여주시 41670', '양평군 41830', '고양시 41280', '구리시 41310', '남양주시 41360',\
                                     '동두천시 41250', '양주시 41630', '의정부시 41150', '파주시 41480', '포천시 41650', '연천군 41800', '가평군 41820'] """)


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

#텔레그램 봇 객체 생성
bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

#listening으로 기다림
bot.message_loop(handle)
print('Listening...')

while 1:
  time.sleep(10)