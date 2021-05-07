
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from selenium.webdriver.common.action_chains import ActionChains
import time

driver=webdriver.Chrome()
driver.get("https://www.err.ee/uudised")

portal = []
article_tags = []
article_headers = []
article_dates = []
article_body = []
article_link = []


for i in range(7):
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in soup.find('div', attrs={'class':'left-block'}).findAll('a', href=True):
        article_link.append(a.get('href'))

    nupud = driver.find_elements_by_css_selector(".history-btn")
    actions = ActionChains(driver)
    actions.move_to_element(nupud[2])
    actions.click(nupud[2])
    actions.perform()
    time.sleep(1)


for i in article_link:
    driver.get(i)
    article_soup = BeautifulSoup(driver.page_source)
    article = None
    time = None
    

    if (article_soup.find('article', attrs={'class':"prime hasPhoto no-border"}) is not None): 
        article = article_soup.find('article', attrs={'class':"prime hasPhoto no-border"})
    elif (article_soup.find('article', attrs={'class':"prime hasMedia hasPhoto no-border"}) is not None):
        article = article_soup.find('article', attrs={'class':"prime hasMedia hasPhoto no-border"})
    elif (article_soup.find('article', attrs={'class':"prime hasPhoto hasGallery no-border"}) is not None):
        article = article_soup.find('article', attrs={'class':"prime hasPhoto hasGallery no-border"})
    elif (article_soup.find('article', attrs={'class':"prime hasMedia hasPhoto hasGallery no-border"}) is not None):
        article = article_soup.find('article', attrs={'class':"prime hasMedia hasPhoto hasGallery no-border"})
    else:
        print("There is a problem with this article:", i)
        continue

    if(article_soup.find('time', attrs={'class':"pubdate ng-binding"}) is not None):
        time = article.find('time', attrs={'class':"pubdate ng-binding"})['title']
    elif(article_soup.find('span', attrs={'class':"pubdate ng-binding"}) is not None):
        time = article.find('span', attrs={'class':"pubdate ng-binding"})['title']
    else:
        print("There is a problem with time", i) 
        continue
    header = article.find('h1').get_text()
    tag =  article.find('div', attrs={'class':"category"}).get_text()
    body = article.find('div', attrs={'class':"text flex-row"}).get_text()
    
    portal.append('err')
    article_tags.append(tag)
    article_headers.append(header)
    article_dates.append(time)
    article_body.append(body)

    print(time)

df = pd.DataFrame({'portal_name':portal,'date':article_dates, 'tag':article_tags, 'link':article_link, 'header':article_headers, 'article':article_body}) 
df.to_csv("C:\\Users\\annal\\Documents\\NLP\\andmekraapimine\\articles.csv", index=False, encoding='utf-8')