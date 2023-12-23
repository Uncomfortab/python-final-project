from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
#import requests
#import sys
# random 'https://zh.wikipedia.org/wiki/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2'
def search(data:dict, tbs:list):
    url = tbs[0]

    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.title.text[:-15]
    #print(title)

    par = soup.p
    #print(par.text)
    tx = par.text
    i = 0
    while i < len(tx):
        if tx[i] == '[':
            tx = tx[:i] + tx[i+3:]
        else:
            i += 1

    driver2 = webdriver.Chrome()
    driver2.get(f'https://www.google.com/search?q={title}')
    soup2 = BeautifulSoup(driver2.page_source, 'html.parser')

    num = soup2.find('div', {"id":"result-stats"}).text
    num = num[:-19]
    num = num[3:]
    num = int(num.replace(',',''))
    #print(num)

    data[url] = [title, tx, num]

    while len(data)+len(tbs) < 5:
        for link in par.find_all('a'):
            link = link.get('href')
            tba = []
            if link[:7] == '/wiki/%':
                link = 'https://zh.wikipedia.org' + link
                tba.append(link)
                if link in data.keys() or link in tbs:
                    tba.pop()
            if len(tba) == 0: # no new links could be followed
                break
            else:
                for lk in tba:
                    tbs.append(lk)

    tbs.pop(0)

data = dict()
tbs = ['https://zh.wikipedia.org/wiki/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2']
while len(tbs) > 0:
    search(data, tbs)
with open('crawl-random.txt', mode='a', encoding='utf-8') as f:
    print(data, file=f)