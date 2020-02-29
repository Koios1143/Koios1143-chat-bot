# -*- coding: UTF-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import csv
import json
import time
import requests
from logger import logger

app = Flask(__name__)

# change zipcode to area
def zipcode_decoder(code):
    area = ' '
    data = '{"100":"臺北市中正","103":"臺北市大同","104":"臺北市中山","105":"臺北市松山","106":"臺北市大安","108":"臺北市萬華","110":"臺北市信義","111":"臺北市士林","112":"臺北市北投","114":"臺北市內湖","115":"臺北市南港","116":"臺北市文山","200":"基隆市仁愛","201":"基隆市信義","202":"基隆市中正","203":"基隆市中山","204":"基隆市安樂","205":"基隆市暖暖","206":"基隆市七堵","207":"新北市萬里","208":"新北市金山","220":"新北市板橋","221":"新北市汐止","222":"新北市深坑","223":"新北市石碇","224":"新北市瑞芳","226":"新北市平溪","227":"新北市貢寮","231":"新北市新店","232":"新北市坪林","233":"新北市烏來","234":"新北市永和","235":"新北市中和","236":"新北市土城","237":"新北市三峽","238":"新北市樹林","239":"新北市鶯歌","241":"新北市三重","242":"新北市新莊","243":"新北市泰山","244":"新北市林口","247":"新北市蘆洲","248":"新北市五股","249":"新北市八里","251":"新北市淡水","252":"新北市三芝","253":"新北市石門","260":"宜蘭縣宜蘭","261":"宜蘭縣頭城","262":"宜蘭縣礁溪","263":"宜蘭縣壯圍","264":"宜蘭縣員山","265":"宜蘭縣羅東","266":"宜蘭縣三星","267":"宜蘭縣大同","268":"宜蘭縣五結","269":"宜蘭縣冬山","270":"宜蘭縣蘇澳","272":"宜蘭縣南澳","209":"連江縣南竿","210":"連江縣北竿","211":"連江縣莒光","212":"連江縣東引","300":"新竹市東區","300":"新竹市北區","300":"新竹市香山","302":"新竹縣竹北","303":"新竹縣湖口","304":"新竹縣新豐","305":"新竹縣新埔","306":"新竹縣關西","307":"新竹縣芎林","308":"新竹縣寶山","310":"新竹縣竹東","311":"新竹縣五峰","312":"新竹縣橫山","313":"新竹縣尖石","314":"新竹縣北埔","315":"新竹縣峨眉","320":"桃園市中壢","324":"桃園市平鎮","325":"桃園市龍潭","326":"桃園市楊梅","327":"桃園市新屋","328":"桃園市觀音","330":"桃園市桃園","333":"桃園市龜山","334":"桃園市八德","335":"桃園市大溪","336":"桃園市復興","337":"桃園市大園","338":"桃園市蘆竹","350":"苗栗縣竹南","351":"苗栗縣頭份","352":"苗栗縣三灣","353":"苗栗縣南庄","354":"苗栗縣獅潭","356":"苗栗縣後龍","357":"苗栗縣通霄","358":"苗栗縣苑裡","360":"苗栗縣苗栗","361":"苗栗縣造橋","362":"苗栗縣頭屋","363":"苗栗縣公館","364":"苗栗縣大湖","365":"苗栗縣泰安","366":"苗栗縣銅鑼","367":"苗栗縣三義","368":"苗栗縣西湖","369":"苗栗縣卓蘭","400":"臺中市中區","401":"臺中市東區","402":"臺中市南區","403":"臺中市西區","404":"臺中市北區","406":"臺中市北屯","407":"臺中市西屯","408":"臺中市南屯","411":"中縣太平","412":"中縣大里","413":"中縣霧峰","414":"中縣烏日","420":"中縣豐原","421":"中縣后里","422":"中縣石岡","423":"中縣東勢","424":"中縣和平","426":"中縣新社","427":"中縣潭子","428":"中縣大雅","429":"中縣神岡","432":"中縣大肚","433":"中縣沙鹿","434":"中縣龍井","435":"中縣梧棲","436":"中縣淸水","437":"中縣大甲","438":"中縣外埔","439":"中縣大安","500":"彰化縣彰化","502":"彰化縣芬園","503":"彰化縣花壇","504":"彰化縣秀水","505":"彰化縣鹿港","506":"彰化縣福興","507":"彰化縣線西","508":"彰化縣和美","509":"彰化縣伸港","510":"彰化縣員林","511":"彰化縣社頭","512":"彰化縣永靖","513":"彰化縣埔心","514":"彰化縣溪湖","515":"彰化縣大村","516":"彰化縣埔鹽","520":"彰化縣田中","521":"彰化縣北斗","522":"彰化縣田尾","523":"彰化縣埤頭","524":"彰化縣溪州","525":"彰化縣竹塘","526":"彰化縣二林","527":"彰化縣大城","528":"彰化縣芳苑","529":"彰化縣二水","540":"南投縣南投","541":"南投縣中寮","542":"南投縣草屯","544":"南投縣國姓","545":"南投縣埔里","546":"南投縣仁愛","551":"南投縣名間","552":"南投縣集集","553":"南投縣水里","555":"南投縣魚池","556":"南投縣信義","557":"南投縣竹山","558":"南投縣鹿谷","600":"嘉義市東區","600":"嘉義市西區","602":"嘉義縣番路","603":"嘉義縣梅山","604":"嘉義縣竹崎","605":"嘉義縣阿里山","606":"嘉義縣中埔","607":"嘉義縣大埔","608":"嘉義縣水上","611":"嘉義縣鹿草","612":"嘉義縣太保","613":"嘉義縣朴子","614":"嘉義縣東石","615":"嘉義縣六腳","616":"嘉義縣新港","621":"嘉義縣民雄","622":"嘉義縣大林","623":"嘉義縣溪口","624":"嘉義縣義竹","625":"嘉義縣布袋","630":"雲林縣斗南","631":"雲林縣大埤","632":"雲林縣虎尾","633":"雲林縣土庫","634":"雲林縣褒忠","635":"雲林縣東勢","636":"雲林縣臺西","637":"雲林縣崙背","638":"雲林縣麥寮","640":"雲林縣斗六","643":"雲林縣林內","646":"雲林縣古坑","647":"雲林縣莿桐","648":"雲林縣西螺","649":"雲林縣二崙","651":"雲林縣北港","652":"雲林縣水林","653":"雲林縣四湖","654":"雲林縣元長","700":"臺南市中西區","701":"臺南市東區","702":"臺南市南區","704":"臺南市北區","708":"臺南市安平","709":"臺南市安南","710":"臺南市永康","711":"臺南市歸仁","712":"臺南市新化","713":"臺南市左鎮","714":"臺南市玉井","715":"臺南市楠西","716":"臺南市南化","717":"臺南市仁德","718":"臺南市關廟","719":"臺南市龍崎","720":"臺南市官田","721":"臺南市麻豆","722":"臺南市佳里","723":"臺南市西港","724":"臺南市七股","725":"臺南市將軍","726":"臺南市學甲","727":"臺南市北門","730":"臺南市新營","731":"臺南市後壁","732":"臺南市白河","733":"臺南市東山","734":"臺南市六甲","735":"臺南市下營","736":"臺南市柳營","737":"臺南市鹽水","741":"臺南市善化","742":"臺南市大內","743":"臺南市山上","744":"臺南市新市","745":"臺南市安定","800":"高雄市新興","801":"高雄市前金","802":"高雄市苓雅","803":"高雄市鹽埕","804":"高雄市鼔山","805":"高雄市旗津","806":"高雄市前鎮","807":"高雄市三民","811":"高雄市楠梓","812":"高雄市小港","813":"高雄市左營","814":"高雄市仁武","815":"高雄市大社","820":"高雄市岡山","821":"高雄市路竹","822":"高雄市阿蓮","823":"高雄市田寮","824":"高雄市燕巢","825":"高雄市橋頭","826":"高雄市梓官","827":"高雄市彌陀","828":"高雄市永安","829":"高雄市湖內","830":"高雄市鳳山","831":"高雄市大寮","832":"高雄市林園","833":"高雄市鳥松","840":"高雄市大樹","842":"高雄市旗山","843":"高雄市美濃","844":"高雄市六龜","845":"高雄市內門","846":"高雄市杉林","847":"高雄市甲仙","848":"高雄市桃源","849":"高雄市那瑪夏","851":"高雄市茂林","852":"高雄市茄定","880":"澎湖縣馬公","881":"澎湖縣西嶼","882":"澎湖縣望安","883":"澎湖縣七美","884":"澎湖縣白沙","885":"澎湖縣湖西","890":"金門縣金沙","891":"金門縣金湖","892":"金門縣金寜","893":"金門縣金城","894":"金門縣烈嶼","896":"金門縣烏坵","900":"屏東縣竹田","901":"屏東縣三地門","902":"屏東縣霧臺","903":"屏東縣瑪家","904":"屏東縣九如","905":"屏東縣里港","906":"屏東縣高樹","907":"屏東縣鹽埔","908":"屏東縣長治","909":"屏東縣麟洛","911":"屏東縣竹田","912":"屏東縣內埔","913":"屏東縣萬丹","920":"屏東縣潮州","921":"屏東縣泰武","922":"屏東縣來義","923":"屏東縣萬巒","924":"屏東縣崁頂","925":"屏東縣新埤","926":"屏東縣南州","927":"屏東縣林邊","928":"屏東縣東港","929":"屏東縣珫球","931":"屏東縣佳冬","932":"屏東縣新園","940":"屏東縣枋寮","941":"屏東縣枋山","942":"屏東縣春日","943":"屏東縣獅子","944":"屏東縣車城","945":"屏東縣牡丹","946":"屏東縣恒春","947":"屏東縣滿州","950":"東縣臺東","951":"東縣綠島","952":"東縣蘭嶼","953":"東縣延平","954":"東縣卑南","955":"東縣鹿野","956":"東縣關山","957":"東縣海端","958":"東縣池上","959":"東縣東河","961":"東縣成功","962":"東縣長濱","963":"東縣太麻里","964":"東縣金峰","965":"東縣大武","966":"東縣達仁","970":"花蓮縣花蓮","971":"花蓮縣新城","972":"花蓮縣秀林","973":"花蓮縣吉安","974":"花蓮縣壽豐","975":"花蓮縣鳳林","976":"花蓮縣光復","977":"花蓮縣豐演","978":"花蓮縣瑞穗","979":"花蓮縣萬榮","981":"花蓮縣玉里","982":"花蓮縣卓溪","983":"花蓮縣富里","817":"東沙群島","819":"南沙群島","290":"釣魚臺"}'
    pos = json.loads(data)
    try:
        area = pos[str(code)]
    except:
        area = '-1'
    return area

def get_nowtime():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
log_file = open('logs.txt','a')

def get_data(url):
    r = requests.get(url)
    try:
        with open('./maskdata.csv','wb') as f:
            f.write(r.content)
            app.logger.info('[get_data] open maskdata.csv -> Success')
            return True
    except:
        app.logger.WARNING('[get_data] open maskdata.csv -> Failed')

def all_num(s):
    for i in s:
        if(not(ord(i) >= ord('0') and ord(i) <= ord('9'))):
            return False
    return True

ret_table = []
store_tot = 0
store_out = 1
# find masks
def get_masks(zipcode):
    if(zipcode == -1):
        app.logger.error('[get_masks] zipcode error')
        return False
    global ret_table
    global store_tot
    output = []
    area = zipcode_decoder(zipcode)
    if(area == '-1'):
        app.logger.error('[get_masks] zipcode doesn\'t exist')
        return False
    app.logger.info('=== processing ===')

    # download file
    app.logger.info('=== downloading files ===')
    url = 'https://data.nhi.gov.tw/resource/mask/maskdata.csv'
    get_data(url)
    app.logger.info('=== download completed ===')

    # load data
    data_name = 'maskdata.csv'
    try:
        with open(data_name, newline='') as csvfile:
            app.logger.info('[get_masks] open maskdata.csv -> Success')
            rows = csv.reader(csvfile)
            for row in rows:
                address = row[2]
                if(address[0] == '台'):
                    address = '臺' + address[1:]
                region = address[0:5]
                if(area == region):
                    store_tot += 1
                    ret_table.append(str('名稱: ' + row[1] + '\n地址: ' + row[2] + '\n成人口罩剩餘數: ' + row[4] + '\n兒童口罩剩餘數: ' + row[5] + '\n來源資料時間: ' + row[6] + '\n\n'))
    except:
        app.logger.WARNING('[get_masks] open maskdata.csv -> Failed')
    return  True

# Channel Access Token
line_bot_api = LineBotApi('hu0lbMP6jvn1xFM+ibTdrXGYQ25reDYjmUQYnNJDjpgWJn7n/xKVPQxnbIFWbpBlVCYj+pxvh8mXoyjtq3cbpQy3Kqz2Djmb4qv6BlUH3Flh0aGt4k6RYnMF8tD+Gcz1ndD+3mpccLFKr4YJNpHaygdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f06829dd46601f40fafec5a96448bec9')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
# Bot information
name = "Koios1143"
in_zipcode = -1
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global ret_table
    global in_zipcode
    global store_tot
    global store_out
    text=event.message.text
    retext = ''
    if text == "--help":
        app.logger.info('[call] --help')
        retext = '''whoami
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
    elif text == "whoami":
        app.logger.info('[call] whoami')
        retext = name
    elif text[0:4].lower() == 'mask':
        app.logger.info('[call] mask' + text[4:])
        #initialize
        ret_table = []
        store_out = 1
        store_tot = 0
        in_zipcode = -1
        text = (str)(text).replace(' ','')
        text = (str)(text).replace('[','')
        text = (str)(text).replace(']','')
        text = (str)(text).replace('+','')
        if(len(text)>=7 and all_num(text[4:7]) == True):
            in_zipcode = int(text[4:7])
        else:
            retext = '輸入格式錯誤!\n查詢格式為:mask+郵遞區號前三碼\n例如查詢永康區輸入:mask710\n'
            app.logger.WARNING('[mask] input format ERROR')
        if(get_masks(in_zipcode) == True):
            flag = 0
            if(len(ret_table)>=10):
                retext += '目前輸出第 ' + str(store_out) + '~' + str(store_out+9) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
                app.logger.info('[mask] output ' + str(store_out) + '~' + str(store_out + 9))
            else:
                retext += '目前輸出第 ' + str(store_out) + '~' + str(store_out+len(ret_table)-1) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n\n'
                app.logger.info('[mask] output ' + str(store_out) + '~' + str(store_out + len(ret_table)-1))
            for i in ret_table:
                if(flag == 10):
                    break
                retext += i
                flag += 1
            store_out += flag
            for i in range(flag):
                del ret_table[0]
        else:
            retext = '請輸入正確的郵遞區號!\n查詢格式為:mask+郵遞區號前三碼\n例如查詢永康區輸入:mask710\n\n若要查詢可用指令請輸入--help\n'
            app.logger.WARNING('[mask] zipcode ERROR')
    elif text == '+':
        if(in_zipcode == -1):
            retext = '請先查詢地區!\n\n若要查詢可用指令請輸入--help\n'
            app.logger.WARNING('[+] no area data')
        elif(len(ret_table)<=0):
            retext = '沒有其他資料囉!\n'
            in_zipcode = -1
            app.logger.info('[+] no other data')
        else:
            if(len(ret_table) >= 10):
                retext += '目前輸出第 ' + str(store_out) + '~' + str(store_out+9) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n'
                app.logger.info('[+] output ' + str(store_out) + '~' + str(store_out + 9))
            else:
                retext += '目前輸出第 ' + str(store_out) + '~' + str(store_out+len(ret_table)-1) + ' 筆資料 , 全部共 ' + str(store_tot) + ' 筆\n'
                app.logger.info('[+] output ' + str(store_out) + '~' + str(store_out + len(ret_table)))
            flag = 0
            for i in ret_table:
                if(flag == 10):
                    break
                retext += i
                flag += 1
            store_out += flag
            for i in range(flag):
                del ret_table[0]
    elif(text[0:7].lower() == 'zipcode'):
        text = (str)(text).replace(' ','')
        try:
            with open('tw-zipcode.json','r') as jsonfile:
                app.logger.info('[zipcode] open tw-zipcode.json -> Success')
                data = json.load(jsonfile)
                city = ''
                if(text[7:9] == '南海'):
                    city = text[7:11]
                    region = text[11:]
                else:
                    city = text[7:10]
                    region = text[10:]
                    region.replace('\n',' ')
                    if(city[0] == '臺'):
                        city = '台' + city[1:]
                try:
                    res = data[city][region]
                    retext = text[7:] + '的郵遞區號為: ' + (str)(res)
                    app.logger.info('[zipcode] output ' + (str)(res))
                except:
                    retext = '輸入錯誤!\n請確認輸入是否完整城市名稱以及區域名稱\n例如查詢台南市永康區:zipcode台南市永康區\n\n若要查詢可用指令請輸入--help\n'
                    app.logger.WARNING('[zipcode] input ERROR')
        except:
            app.logger.ERROR('[zipcode] open tw-zipcode,json -> ERROR')
    else:
        retext = (text + "です\n")
        app.logger.info('[other] output ' + text + 'です')
    app.logger.info('retext size: ' + str(len(retext)))
    message = TextSendMessage(retext)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
