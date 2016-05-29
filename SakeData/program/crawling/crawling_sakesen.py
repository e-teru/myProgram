import requests
from bs4 import BeautifulSoup
import string
import re
import codecs
import time
import json

length = 800
start_urls = [] * length
html_number = 1
_id = 1
sake = {}
for a in range(1,length):
  sake[a] = {}
for var in range(1,length):
  domain = 'http://www.sake-sennin.com'
  url = "http://www.sake-sennin.com/fbo/web/app.php/user/product/"+str(html_number)
  r = requests.get(url)
  soup = BeautifulSoup(r.text.encode(r.encoding),"html.parser")
  flag = 0
  flag_koumi = 0
  flag_target = 0
  flag_temp = 0
  flag_glass = 0
  flag_dish = 0
  bre_url=''
  try:
    bre_info = soup.find('div', attrs={'id':'detail-title'}) 
    bre_url = bre_info.find('li', attrs={'id':'tab4'}).a.get('href')
    #sake[_id][]=domain+bre_url)
    #酒造情報記載ページから情報取得
    #r1 = requests.get(bre_url)
    #brewery = BeautifulSoup(r1.text.encode(r.encoding),"html.parser")
    #table_bre = soup.find('div', attrs={'id':'kuramoto-box1'}) 

    photo = soup.find('div',attrs={'id':'mainphoto'})
    sake[_id]['画像URL'] = domain+photo.img['src']   
    table1 = soup.find('div', attrs={'id':'sake-box1'}) 
    sake_area = table1.find('div', attrs={'id':'area'}).text
    sake_name = table1.find('h4').text
    sake_genre = table1.find('div', attrs={'id':'genre'}).text.lstrip().strip()
    test = table1.find('dl', attrs={'class':'sake1'})
    if test.findAll('dt')[0].text =='蔵元名':
      bre = test.findAll('dd')[0].text
    if test.findAll('dt')[1].text =='製造年月日':
      year = test.findAll('dd')[1].text
    if test.findAll('dt')[2].text =='容量':
      size = test.findAll('dd')[2].text
    if test.findAll('dt')[3].text =='メーカー希望小売価格':
      cost = test.findAll('dd')[3].text.replace(',','')
    if test.findAll('dt')[4].text =='主な受賞など':
      award = test.findAll('dd')[4].text

    
    sake[_id]['名前']=sake_name
    sake[_id]['URL']=url
    sake[_id]['都道府県']=sake_area
    sake[_id]['種類']=sake_genre
    sake[_id]['蔵元']=bre
    sake[_id]['製造年月日']=year
    sake[_id]['容量']=size
    sake[_id]['メーカー希望小売価格']=cost
    sake[_id]['主な受賞歴など']=award

    table2 = soup.find('table', attrs={'class':'kome-haigou'}) 
    rice = table2.find('th').text.strip().replace(' ','').replace('\n','').replace('<使用米>' ,'')
    rice1 = table2.findAll('td')[0].text.strip().replace(' ','').replace('\n','').replace('＜掛米＞','')
    rice2 = table2.findAll('td')[1].text.strip().replace(' ','').replace('\n','').replace('＜麹米＞','')
    sake[_id]['使用米']=rice
    sake[_id]['麹米']=rice1
    sake[_id]['掛米']=rice2

    test = table1.find('dl', attrs={'class':'sake2'})
    if test.findAll('dt')[0].text =='使用酵母 ':
      yeast = test.findAll('dd')[0].text
    if test.findAll('dt')[1].text =='酒母（酛）':
      syubo = test.findAll('dd')[1].text
    if test.findAll('dt')[2].text =='アルコール度数 ':
      alcohol = test.findAll('dd')[2].text
    if test.findAll('dt')[3].text =='日本酒度 ':
      nihonsyudo = test.findAll('dd')[3].text
    if test.findAll('dt')[4].text =='酸度 ':
      sando = test.findAll('dd')[4].text
    if test.findAll('dt')[5].text =='アミノ酸度 ':
      amino = test.findAll('dd')[5].text
    if test.findAll('dt')[6].text =='その他':
      other = test.findAll('dd')[6].text

    sake[_id]['使用酵母']=yeast
    sake[_id]['酒母（酛）']=syubo
    sake[_id]['アルコール度数']=alcohol
    sake[_id]['日本酒度']=nihonsyudo
    sake[_id]['酸度']=sando
    sake[_id]['アミノ酸度']=amino
    sake[_id]['その他']=other


    table3 = soup.find('div', attrs={'id':'sake-photo'}) 
    for tr in table3.findAll('tr'):
      #sake[_id][]=tr.find('th').text)
      if flag == 1:
        if flag_koumi==1:
          sake[_id]['香味']=tr.find('td').string.lstrip()
          flag_koumi=0
          flag = 0
        if flag_target==1:
          sake[_id]['適した飲用シーンとターゲット例']=tr.find('td').string.lstrip()
          flag_target=0
          flag = 0
        if flag_temp==1:
          sake[_id]['適した飲用温度例']=tr.find('td').string.lstrip()
          flag_temp=0
          flag = 0
        if flag_glass==1:
          sake[_id]['適した酒器例']=tr.find('td').string.lstrip()
          flag_glass=0
          flag = 0
        if flag_dish==1:
          sake[_id]['相性の良い料理例']=tr.find('td').string.lstrip()
          flag_dish=0
          flag = 0
      elif flag == 0:
        str1 = tr.find('th').text.replace('※詳しくはこちら','')
        #sake[_id][]=str1)
        if str1==' 香味の特徴':
          #sake[_id][]='香味')
          flag_koumi=1
          flag = 1
          #sake[_id][]=tr.find('td').string)
        if str1=='適した飲用ｼｰﾝとﾀﾞｰｹﾞｯﾄ例':
          #sake[_id][]='香味')
          flag_target=1
          flag = 1
        if str1=='適した飲用温度例':
          #sake[_id][]='香味')
          flag_temp=1
          flag = 1
        if str1=='適した酒器例':
          #sake[_id][]='香味')
          flag_glass=1
          flag = 1
        if str1=='相性の良い料理例':
          #sake[_id][]='香味')
          flag_dish=1
          flag = 1
    print('日本酒'+str(html_number)+":Success!")
    _id = _id + 1
    length = length + 1
  except AttributeError:
    print('日本酒'+str(html_number)+":AttributeError")
  html_number = html_number + 1
  time.sleep(1)
f = codecs.open('../../sake_data/json/sake_sen.json','w','utf-8')
json.dump(sake, f, sort_keys=True, ensure_ascii=False,indent = 2)
f.close()
#https://json-csv.com
