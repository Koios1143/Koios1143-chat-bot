# -*- coding: UTF-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import sys
sys.path.append('subroutine/')
print(sys.path)

from logger import logger

import csv
import json
import time
import requests
import get_data
import yaml
import get_distance
import add_pos
import datetime

app = Flask(__name__)

# get line token
config = open('config.yml', 'r', newline='')
cfg = yaml.load(config)
LINE_ACCESS_TOKEN = cfg['LINE']['ACCESS_TOKEN']
LINE_SECRET = cfg['LINE']['SECRET']

# change zipcode to area
def zipcode_decoder(code):
    area = ' '
    try:
        with open('./data/tw-zipcode_de.json','r')as jsonfiles:
            data = json.load(jsonfiles)
            logger.info('open tw-zipcode_de.json -> Success')
            try:
                area = data[str(code)]
            except:
                logger.warning('[zipcode_decoder] code ERROR')
                area = '-1'
            return area
    except:
        logger.error('[zipcode_decoder] open tw-zipcode_de.json -> Failes')

# get now time
def get_nowtime():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# check if all numbers
def all_num(s):
    for i in s:
        if(not(ord(i) >= ord('0') and ord(i) <= ord('9'))):
            return False
    return True

# check if need update
def update():
    now = datetime.datetime.now()
    s = ''
    with open('data/maskdata.csv','r',newline='') as f:
        data = csv.reader(f)
        flag = 0
        for i in data:
            if(flag == 1):
                s = i[6]
                break
            else:
                flag += 1
    s.replace('\n','')
    print(s)
    past = datetime.datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
    minutes = datetime.timedelta(minutes=30)
    if(now-past>=minutes):
        get_data.get_maskdata()
        add_pos.add_pos()
        return True
    else:
        return False

ret_table = []
store_tot = 0
store_out = 1
# find masks
def get_masks(area):
    if(in_zipcode == -1):
        logger.error('[get_masks] zipcode error')
        return False
    global ret_table
    global store_tot
    output = []
    if(area == '-1'):
        logger.error('[get_masks] zipcode doesn\'t exist')
        return False

    # load data
    data_name = './data/maskdata.csv'
    YN = False
    try:
        with open(data_name, newline='') as csvfile:
            logger.info('[get_masks] open maskdata.csv -> Success')
            rows = csv.reader(csvfile)
            for row in rows:
                address = row[2]
                if(address[0] == '台'):
                    address = '臺' + address[1:]
                region = address[0:5]
                if(area == region):
                    store_tot += 1
                    s = ''
                    if(YN == True):
                        s = '\n\n'
                    else:
                        YN = True
                    s = s + str('名稱: ' + row[1] + '\n地址: ' + row[2] + '\n成人口罩剩餘數: ' + row[4] + '\n兒童口罩剩餘數: ' + row[5] + '\n來源資料時間: ' + row[6])
                    ret_table.append(s)
    except:
        logger.warning('[get_masks] open maskdata.csv -> Failed')
    return  True

# ------------------- type: text request -------------------
def call_help():
    logger.info('[call] --help')
    s = '''whoami
    回覆我的名稱
mask+郵遞區號前三碼
    查詢該區域內口罩剩餘數量
    例如要查詢台南市永康區的口罩數量:mask710
+
    回覆口罩查詢更多結果
zipcode+[城市(縣/市)][區域(鄉/鎮/市/區)]
    回覆該區域的郵遞區號(三碼)
    例如要查詢台南市永康區:zipcode台南市永康區
--help
    回覆可用指令'''
    return s

def call_whoami():
    logger.info('[call] whoami')
    return 'Koios1143'

def call_mask(texts):
    global ret_table
    global store_out
    global store_tot
    global in_zipcode
    logger.info('[call] mask' + texts[4:])
    #initialize
    ret_table = []
    store_out = 1
    store_tot = 0
    in_zipcode = -1
    texts = (str)(texts).replace(' ','')
    texts = (str)(texts).replace('[','')
    texts = (str)(texts).replace(']','')
    texts = (str)(texts).replace('+','')
    if(len(texts)>=7 and all_num(texts[4:7]) == True):
        in_zipcode = int(texts[4:7])
    else:
        logger.warning('[mask] input format ERROR')
        return '輸入格式錯誤!\n查詢格式為:mask+郵遞區號前三碼\n例如查詢永康區輸入:mask710\n\n若要查詢郵遞區號可使用zipcode指令\n\n若要查詢可用指令請輸入--help'
    s = ''
    if(get_masks(zipcode_decoder(in_zipcode)) == True):
        flag = 0
        if(len(ret_table)>=10):
            s += '目前輸出第 ' + str(store_out) + '~' + str(store_out+9) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
            logger.info('[mask] output ' + str(store_out) + '~' + str(store_out + 9))
        else:
            s += '目前輸出第 ' + str(store_out) + '~' + str(store_out+len(ret_table)-1) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
            logger.info('[mask] output ' + str(store_out) + '~' + str(store_out + len(ret_table)-1))
        for i in ret_table:
            if(flag == 10):
                break
            s += i
            flag += 1
        store_out += flag
        for i in range(flag):
            del ret_table[0]
        return s
    else:
        logger.warning('[mask] zipcode ERROR')
        return '請輸入正確的郵遞區號!\n查詢格式為:mask+郵遞區號前三碼\n例如查詢永康區輸入:mask710\n\n若要查詢可用指令請輸入--help'
    
def call_plus():
    global in_zipcode
    global ret_table
    global store_out
    global store_tot
    if(in_zipcode == -1):
        logger.warning('[+] no area data')
        return '請先查詢地區!\n\n若要查詢郵遞區號，請使用zipcode指令\n若要查詢可用指令請輸入--help'
    elif(len(ret_table)<=0):
        in_zipcode = -1
        logger.info('[+] no other data')
        return '沒有其他資料囉!'
    else:
        s = ''
        if(len(ret_table) >= 10):
            s += '目前輸出第 ' + str(store_out) + '~' + str(store_out+9) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
            logger.info('[+] output ' + str(store_out) + '~' + str(store_out + 9))
        else:
            s += '目前輸出第 ' + str(store_out) + '~' + str(store_out+len(ret_table)-1) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
            logger.info('[+] output ' + str(store_out) + '~' + str(store_out + len(ret_table)-1))
        flag = 0
        for i in ret_table:
            if(flag == 10):
                break
            s += i
            flag += 1
        store_out += flag
        for i in range(flag):
            del ret_table[0]
        return s

def call_zipcode(texts):
    texts = (str)(texts).replace(' ','')
    try:
        with open('./data/tw-zipcode.json','r') as jsonfile:
            logger.info('[zipcode] open tw-zipcode.json -> Success')
            data = json.load(jsonfile)
            if(texts[7:9] == '南海'):
                city = texts[7:11]
                region = texts[11:]
            else:
                city = texts[7:10]
                region = texts[10:]
                region.replace('\n',' ')
                if(city[0] == '臺'):
                    city = '台' + city[1:]

            try:
                res = data[city][region]
                logger.info('[zipcode] output ' + (str)(res))
                return (texts[7:] + '的郵遞區號為: ' + (str)(res))
            except:
                logger.warning('[zipcode] input ERROR')
                return '輸入錯誤!\n請確認輸入是否完整城市名稱以及區域名稱\n例如查詢台南市永康區:zipcode台南市永康區\n\n若要查詢可用指令請輸入--help'
    except:
        logger.error('[zipcode] open tw-zipcode.json -> ERROR')
        return '[call_zipcode] tw-zipcode.json 檔案開啟失敗'

def call_default(texts):
    logger.info('[other] output ' + texts + 'です')
    return (texts + "です")

# ------------------- type: location request ----------------------
def loc_mask(event):
    lat1 = float(event.message.latitude)
    lng1 = float(event.message.longitude)
    r = 1 #km
    tot = 0
    ret = ''
    with open('data/maskdata_pos.csv', 'r') as f:
        data = csv.reader(f)
        YN = False
        for i in data:
            lat2 = float(i[7])
            lng2 = float(i[8])
            if(get_distance.distance(lat1,lng1,lat2,lng2) <= r):
                s = ''
                if(YN==True):
                    ret = ret + '\n\n'
                else:
                    YN=True
                name = '名稱: ' + str(i[1])
                location = '地址: ' + str(i[2])
                tel = '電話: ' + str(i[3])
                man_mask = '成人口罩: ' + str(i[4])
                ch_mask = '兒童口罩: ' + str(i[5])
                time = '最後更新時間: ' + str(i[6])
                ret = ret + name + '\n' + location + '\n' + tel + '\n' + man_mask + '\n' + ch_mask + '\n' + time
                tot += 1
    ret = '共找到 ' + str(tot) + '筆資料\n' + ret
    logger.info('共找到 ' + str(tot) + '筆資料')
    return ret

# Channel Access Token
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(LINE_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
in_zipcode = -1
# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    global ret_table
    global in_zipcode
    global store_tot
    global store_out
    ret_type = event.message.type
    logger.info('User: ' + str(event.source.user_id))
    logger.info('message type: ' + str(event.message.type))
    logger.info('source type: ' + str(event.source.type))
    if(ret_type == 'text'):
        text=event.message.text
        retext = ''
        if text == "--help":
            retext = call_help()
        elif text == "whoami":
            retext = call_whoami()
        elif text[0:4].lower() == 'mask':
            update()
            retext = call_mask(text)
        elif text == '+':
            retext = call_plus()
        elif(text[0:7].lower() == 'zipcode'):
            retext = call_zipcode(text)
        else:
            retext = call_default(text)
        logger.info('retext size: ' + str(len(retext)))
        message = TextSendMessage(retext)
        line_bot_api.reply_message(event.reply_token, message)
    elif(ret_type == 'location'):
        update()
        retext = loc_mask(event)
        message = TextSendMessage(retext)
        line_bot_api.reply_message(event.reply_token, message)
    elif(ret_type == 'image'):
        pass
    elif(ret_type == 'video'):
        pass
    elif(ret_type == 'audio'):
        pass
    elif(ret_type == 'file'):
        pass
    elif(ret_type == 'sticker'):
        pass

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
