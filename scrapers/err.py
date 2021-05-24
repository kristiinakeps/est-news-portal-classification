
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
article_links = []

links = []

for i in range(365):
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in soup.find('div', attrs={'class':'left-block'}).findAll('a', href=True):
        links.append(a.get('href'))

    nupud = driver.find_elements_by_css_selector(".history-btn")
    actions = ActionChains(driver)
    actions.move_to_element(nupud[2])
    actions.click(nupud[2])
    actions.perform()
    time.sleep(0.5)

count = len(links)
current = 0
for link in links:
    current += 1
    try:
        driver.get(link)
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
            print("There is a problem with this article:", link)
            continue

        if(article.find('time', attrs={'class':"pubdate ng-binding"}) is not None) :
            time = article.find('time', attrs={'class':"pubdate ng-binding"})['title']
        elif(article.find('span', attrs={'class':"pubdate ng-binding"}) is not None):
            time = article.find('span', attrs={'class':"pubdate ng-binding"})['title']
        else:
            print("There is a problem with time", link)
            continue
        header = article.find('h1').get_text()
        tag =  article.find('div', attrs={'class':"category"}).get_text()
        body = article.find('div', attrs={'class':"text flex-row"}).get_text()

        portal.append('err')
        article_dates.append(time)
        article_tags.append(tag)
        article_headers.append(header)
        article_body.append(body)
        article_links.append(link)

        print(time)
        if current % 10 == 0:
            print(f'{current} of {count} done')
    except:
        print(f'Error with page {link}, skipping')
        df = pd.DataFrame({'portal_name':portal,'date':article_dates, 'tag':article_tags, 'link':article_links, 'header':article_headers, 'article':article_body}) 
        df.to_csv("C:\\Users\\annal\\Documents\\NLP\\andmekraapimine\\bak_articles.csv", index=False, encoding='utf-8')
        df = pd.DataFrame({'links':links})
        df.to_csv("C:\\Users\\annal\\Documents\\NLP\\andmekraapimine\\links.csv", index=False, encoding='utf-8')

df = pd.DataFrame({'portal_name':portal,'date':article_dates, 'tag':article_tags, 'link':article_links, 'header':article_headers, 'article':article_body}) 
df.to_csv("C:\\Users\\annal\\Documents\\NLP\\andmekraapimine\\articles.csv", index=False, encoding='utf-8')
