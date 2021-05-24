
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
links = []
tags = []

def allow_cookies():
    try:
        time.sleep(5)
        notifications = driver.find_element_by_id('onesignal-slidedown-cancel-button')
        actions = ActionChains(driver)
        actions.click(notifications)
        actions.perform()
    except:
        print('cookie feil')

def accept_conditions():
    try:
        time.sleep(5)
        conditions = driver.find_element_by_css_selector("button.fc-button-consent")
        actions = ActionChains(driver)
        actions.click(conditions)
        actions.perform()
    except:
        print('conditions feil')

def log_in():
    time.sleep(3)
    element = driver.find_element_by_css_selector("a.button-digi.button-digi--login.no-mobile-show")
    actions = ActionChains(driver)
    actions.click(element)
    actions.perform()
    email_parool = driver.find_element_by_css_selector("form.page-modal--popup-form.modal-hint--form").find_elements_by_tag_name("input")
    email_parool[0].send_keys('email@gmail.com')
    email_parool[1].send_keys('password')
    element = driver.find_element_by_css_selector("div.page-modal--login-submit")
    actions = ActionChains(driver)
    actions.click(element)
    actions.perform()

def scroll_webpage():
    print('starting scrolling')
    last_article_date = ''
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)
        article_dates = BeautifulSoup(driver.page_source).findAll(
            'div', attrs={'class': "article-unit--date"})
        if "31. oktoober 2021" in last_article_date or last_article_date == article_dates[-1].getText():
            return
        last_article_date = article_dates[-1].getText()
        print(last_article_date)


accept_conditions()
allow_cookies()
log_in()
scroll_webpage()

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
for a in soup.findAll('h6'):
    links.append(a.findAll('a', href=True)[0].get('href'))

count = len(links)
current = 0
for i in links:
    print('count on', count)
    current += 1
    try:
        if 'https' in i:
            url = i
        else:
            url = 'https://www.ohtuleht.ee' + i
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
        for x in article.find('article', attrs={'class':"page-layout--container"}).findAll('p'):
            body += x.get_text()
        

        portal.append('ohtuleht')
        article_headers.append(header)
        article_dates.append(time)
        article_body.append(body)
        article_link.append(url)
        tags.append(tag)
        if current % 10 == 0:
            print(f'{current} of {count} done')
    except:
        print(f'failed with article {i}')



df = pd.DataFrame({
    'portal_name': portal,
    'date': article_dates,
    'tags': tags,
    'link': article_link,
    'header': article_headers,
    'article': article_body,
})

df.to_csv("C:\\Users\\annal\\Documents\\NLP\\andmekraapimine\\articles_ohtuleht_uus.csv", index=False, encoding='utf-8')

