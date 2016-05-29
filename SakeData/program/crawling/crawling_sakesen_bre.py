import requests
from bs4 import BeautifulSoup
import string
import re
import codecs
import time
import json

length = 2000
start_urls = [] * length
html_number = 1
_id = 1
sake = {}
for a in range(1,length):
  sake[a] = {}
for var in range(1,length):
  url = "http://www.sake-sennin.com/fbo/web/app.php/user/brewers/"+str(html_number)
  r = requests.get(url)
  soup = BeautifulSoup(r.text.encode(r.encoding),"html.parser")

  try:
    bre_info =soup.find('div', attrs={'id':'kuramoto-box1'}) 
    sake[_id]['呼び方']=soup.find('div',attrs={'id':'caption'}).text
    for tr in bre_info.table.findAll('tr'):
      if tr.find('th').text=='蔵元名':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='銘柄名の由来':
        sake[_id][tr.find('th').text] = tr.find('td').text  
      elif tr.find('th').text=='代表者名':
        sake[_id][tr.find('th').text] = tr.find('td').text  
      elif tr.find('th').text=='代目':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='創業年':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='杜氏名':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='杜氏の流派':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='出荷石数/年':
        sake[_id][tr.find('th').text] = tr.find('td').text  
      elif tr.find('th').text=='仕込み水（水源名）':
        sake[_id][tr.find('th').text] = tr.find('td').text.replace(' ','').replace('\n','')  
      elif tr.find('th').text=='水質':
        sake[_id][tr.find('th').text] = tr.find('td').text.replace(' ','').replace('\n','')
      elif tr.find('th').text=='住所':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='TEL':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='FAX':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='メーカーサイト':
        sake[_id][tr.find('th').text] = tr.find('td').text
      elif tr.find('th').text=='Email':
        sake[_id][tr.find('th').text] = tr.find('td').text  
    _id = _id + 1
    length = length + 1
    print('蔵元情報'+str(html_number)+":Success!")
  except AttributeError:
    print('蔵元情報'+str(html_number)+":AttributeError")
  html_number = html_number + 1
  time.sleep(1)
f = codecs.open('../../sake_data/json/sake_sen_bre.json','w','utf-8')
json.dump(sake, f, sort_keys=True, ensure_ascii=False,indent = 2)
f.close()
