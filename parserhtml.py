import os,csv,re
from bs4 import BeautifulSoup
import pandas as pd

htmlfile = os.path.join(os.path.dirname(os.getcwd()),'data','appstorerank')
filelist = os.listdir(htmlfile)
csvpath = os.path.join(os.path.dirname(os.getcwd()),'data','output','data.csv')
datepattern = r'^2017\d{2}01'
typepattern = r'appstore[a-z]+'
with open('usedhtml.txt','a+') as ff:
    usedhtml = [i.replace('\n','') for i in ff.readlines()]
for html in filelist:
    if html in usedhtml:
        continue
    filepath = os.path.join(htmlfile,html)
    with open(filepath,'r',encoding = 'utf-8') as f:
        text = f.read()
    date = re.search(datepattern,html).group()
    ranktype = re.search(typepattern,html).group().replace('appstore','')
    soup = BeautifulSoup(text,'html.parser')
    tbody = soup.find('tbody')
    trlist = tbody.find_all('tr')
    for tr in trlist:
        try:
            name = tr.find('a',{'class':'name'})
            appname = name.get_text().replace('\n','')
            appleid = name['href'].replace('/app/rank/appid/','').replace('/country/cn','')
        except:
            print(html,name)
            continue
        try:
            company = tr.find('p',{'class':'company'}).get_text()
        except:
            company = 'na'
        try:
            incname = tr.find('a',{'class':'dark-green'}).get_text()
        except:
            incname = 'na'
        tempdata = [appleid,appname,company,incname,date,ranktype]
        with open(csvpath,'a+',encoding = 'utf-8',newline = '') as csvfile:
            w = csv.writer(csvfile)
            w.writerow(tempdata)
    with open('usedhtml.txt','a+') as f2:
        f2.write('\n{}\n'.format(html))
        
            
