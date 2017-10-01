#!/usr/bin/env python
# coding: UTF-8
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
import time
import twitter

OK = '33[92m'
WARN = '33[93m'
NG = '33[91m'
END_CODE = '33[0m'

api = twitter.Api(consumer_key='ONSjLdQEezB4PFu8Bkc9sdmZB',
                      consumer_secret='OTyi1341jMF2DwU5uMYWZoAZERl4S9mH92Hi58sOPpW4grjq3p',
                      access_token_key='772207710687236096-oTWbHmtHVT4r8a1ujJPEPXUA3wAk2wk',
                      access_token_secret='94iVWZUiSKxGythLOrWR7mS97xxRrtguSVtdbMY72oSEt')

#ScheduledTimes = [datetime.datetime.time(8,30,0),datetime.datetime.time(6,0,0)]
ScheduledTimes = ["8:30","7:15"]
#ScheduledTimes = "23:35"

# アクセスするURL
#url = "https://typhoon.yahoo.co.jp/weather/jp/warn/38/"
#url = "http://www.jma.go.jp/jp/warn/342_table.html"
#url = "https://typhoon.yahoo.co.jp/weather/jp/warn/15/"
url = "https://typhoon.yahoo.co.jp/weather/jp/warn/38/38201/"

#Access and
html = request.urlopen(url).read()


def Getter(soup):
    Summaryarea = soup.findAll("div",class_="warnSummary_box")
    #print(Summaryarea[0].dl)
    Li = Summaryarea[0].dl.dd.ul.li
    #adv = Li.find("span",class_="icoAdvisory")#警報知らせ
    adv = Li.find("span",class_="icoWarning")#注意報知らせ
    if adv:
        #Yes
        #print("OK")
        return 1
    else:
        #No
        #print("NO")
        return 0
def Twit(state):
    nowtime = datetime.now()
    NowStr = str(nowtime.hour) + "時" + str(nowtime.minute) + "分現在"
    Txt = ""
    if state:
        Txt = "\n[警報確認Bot]\n松山市に警報が発令されてるみたい。。。\nべっ別に学校休みだからって喜んだりしないんだからねっ！！"
    else:
        Txt = "\n[警報確認Bot]\n松山市には警報出てないみたいね。\n変な悪あがきはやめてさっさと学校に行くことね。"
    status = api.PostUpdate("[気象警報自動通知システム]"+NowStr+Txt)
    print(status.text)



def Coloring(txt,code):
    return "\033[%sm%s\033[0m" % (code, txt)


def main():
    while 1:
        nowtime = datetime.now()
        ntStr = str(nowtime.hour)+":"+str(nowtime.minute)
        print("Now "+ntStr)
        #Get
        soup = BeautifulSoup(html,"html.parser")
        stat = Getter(soup)
        if stat:
            print(Coloring("!!!!WARNING!!!!","31"))
        else:
            print(Coloring("ALLGREEN","32"))
        if ntStr in ScheduledTimes:
            print("Its time!")
            Twit(stat)

        time.sleep(60)



if __name__ == "__main__":
    main()
