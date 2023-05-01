from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
 
import os
import csv
 
import time
import datetime
 
#------------------------------------
#ユーザー名
UserDir="****"
#------------------------------------
  
#CSVファイル読み込み
cell=[]
f = open("twitter_post.csv",'r', encoding="utf-8")
reader = csv.reader(f)
for row in reader:
    ar=[]
    for r in row:
        ar.append(r)
    cell.append(ar)
f.close()
print(cell)
 
#投稿済みカウントを読み込み
try:
    f = open("twitter_count.txt","r",encoding="utf-8")
    count=int(f.read())
    f.close()
except:
    count=0
 
while count<len(cell):
 
    #投稿予定時間を取得する
    yy=cell[count][0].split('/')
    mm=cell[count][1].split(':')
    nexttime=datetime.datetime(int(yy[0]),int(yy[1]),int(yy[2]), int(mm[0]),int(mm[1]))
    print(nexttime.strftime("%Y/%m/%d %H:%M"))
 
    #投稿予定時間を超えていなければ待つ時間を設定、超えてたら待たずに投稿
    if nexttime>datetime.datetime.now():
        #sleepで待つ時間を指定する
        now=nexttime-datetime.datetime.now()
        time.sleep(now.seconds)
 
 
    #twitterに投稿
    os.system("taskkill /F /IM chrome.exe")
    options = webdriver.ChromeOptions()
      
    pp=r"C:\\Users\\"+UserDir+"\\AppData\\Local\\Google\\Chrome\\User Data"
    options.add_argument('--user-data-dir='+pp)
    options.add_argument('--profile-directory=Default')
      
    web=webdriver.Chrome(options=options)
    web.get("https://twitter.com/home")
 
 
    time.sleep(5)
     
    el=web.find_element_by_class_name("notranslate")
    el.send_keys(cell[count][2])
 
 
    time.sleep(5)
 
    el=web.find_element_by_xpath('//*[@data-testid="tweetButtonInline"]')
    el.click()
 
 
    #投稿済みカウントを記録
    f = open("twitter_count.txt","w",encoding="SHIFT-JIS")
    count=count+1
    f.write(str(count))
    f.close()
 
    time.sleep(5)
    web.quit()