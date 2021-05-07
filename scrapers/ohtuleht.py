
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from selenium.webdriver.common.action_chains import ActionChains
import time

driver=webdriver.Chrome()
driver.get("https://www.ohtuleht.ee/uudised")

portal = []
article_headers = []
article_dates = []
article_body = []
article_link = []
tags = []

def scroll_webpage():
    print('starting')
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        print('sleeping')
        print('slept')
        article_dates = BeautifulSoup(driver.page_source).findAll(
            'div', attrs={'class': "article-unit--date"})
        print('test')
        for date in article_dates:
            print(date)
            if "19. aprill 2021" in date.get_text():
                return

scroll_webpage()

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
for a in soup.findAll('h6'):
    article_link.append(a.findAll('a', href=True)[0].get('href'))

for i in article_link:
    if 'https' in i:
        url = i
    else:
        url = 'https://www.ohtuleht.ee' + i
    print(url)
    driver.get(url)
    article = BeautifulSoup(driver.page_source, features="html.parser")
    article_header = None
    time = None
    

    if (article.find('h1') is not None): 
        article_header = article.find('h1')
    else:
        print("There is a problem with this article header:", i)

    if(article.find('div', attrs={'class': "details--inner"}) is not None):
        time = article.find('div', attrs={'class': "details--inner"}).get_text().split(',')[1]
    else:
        print("There is a problem with time", i)

    header = article.find('h1').get_text()
    tag =  article.find('div', attrs={'class':"article-main--sections"}).get_text()
    body = ''
    for x in article.find('div', attrs={'class':"page-layout--inner"}).findAll('p'):
        body += x.get_text()
    
    portal.append('ohtuleht')
    print(time)
    article_headers.append(header)
    article_dates.append(time)
    article_body.append(body)
    tags.append(tag)


df = pd.DataFrame({
    'portal_name': portal,
    'date': article_dates,
    'tags': tags,
    'link': article_link,
    'header': article_headers,
    'article': article_body,
})
df.to_csv("articles.csv", index=False, encoding='utf-8')
