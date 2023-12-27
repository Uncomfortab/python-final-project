from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
#import sys
# random 'https://zh.wikipedia.org/zh-tw/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2'
def search(data:dict, tbs:list):
    url = tbs[0]

    #driver = webdriver.Chrome()
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.title.text[:-15].encode('utf-8')
    print(title)#

    par = soup.p
    #print(par.text)#
    tx = par.text
    i = 0
    while i < len(tx):
        if tx[i] == '[':
            tx = tx[:i] + tx[i+3:]
        else:
            i += 1
    #print(tx)#
    driver2 = webdriver.Chrome()
    url2 = f'''https://www.google.com/search?q={title.decode('utf-8')}'''
    #print(url2)#
    driver2.get(url2)
    soup2 = BeautifulSoup(driver2.page_source, 'html.parser')
    try:
        num = soup2.find('div', {"id":"result-stats"}).text
        print(num.encode('utf-8'))#
        num = num[:-19]
        num = num[3:]
        num = int(num.replace(',',''))
    except AttributeError:
        print('raised AttributeError. retry connection...')
        driver3 = webdriver.Chrome()
        driver3.get(url2)
        soup2 = BeautifulSoup(driver3.page_source, 'html.parser')
        num = soup2.find('div', {"id":"result-stats"}).text
        print(num.encode('utf-8'))#
        num = num[:-19]
        num = num[3:]
        num = int(num.replace(',',''))
    except ValueError:
        print('raised ValueError. retry connection...')
        driver4 = webdriver.Chrome()
        driver4.get(url2)
        soup2 = BeautifulSoup(driver4.page_source, 'html.parser')
        num = soup2.find('div', {"id":"result-stats"}).text
        print(num.encode('utf-8'))#
        num = num[:-19]
        num = num[3:]
        num = int(num.replace(',',''))
    
    #print(num)

    data[url] = [title.decode('utf-8'), tx, num]
    with open('database01.txt', mode='a', encoding='utf-8') as f:
        print(data[url], file=f)

    if len(data)+len(tbs) < 100:
        tba = []
        for link in par.find_all('a'):
            link = link.get('href')            
            if link[:7] == '/wiki/%':
                link = 'https://zh.wikipedia.org' + link.replace('wiki', 'zh-tw')
                if link.find('#') != -1:
                    link = link[:link.find('#')]
                tba.append(link)
                if link in data.keys() or link in tbs or link in tba:
                    tba.pop()
            '''if len(tba) == 0: # no new links could be followed
                break
            else:'''
        for lk in tba:
            tbs.append(lk)

    tbs.pop(0)

data = dict()

while len(data) < 100:
    tbs = ['https://zh.wikipedia.org/zh-tw/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2']
    while len(tbs) > 0: # a thread from random
        search(data, tbs)

'''with open('crawl-random-rq.txt', mode='a', encoding='utf-8') as f:
    print(data, file=f)'''