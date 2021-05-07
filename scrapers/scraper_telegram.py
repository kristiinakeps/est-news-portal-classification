import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://telegram.ee/'
topics = ['eesti', 'maailm', 'teadus-ja-tulevik', 'toit-ja-tervis', 'kehakultuur', 'vaimsus', 'nwo', 'maavaline', 'arvamus', 'ajaviide']
pages = [35, 43, 22, 31, 2, 24, 21, 11, 17, 11]
news_by_topics = {}

try:
    for i in range(0,  len(topics)):
        news_by_topics[topics[i]] = []
        print(topics[i])
        for j in range(1, pages[i] + 1):
            print(j)
            page_url = '/' if j == 1 else '/page/' + str(j) + '/'
            page = requests.get(URL + topics[i] + page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            news_links = soup.find_all('div', class_='grid-item')
            for news in news_links:
                try:
                    link = news.find('a')['href']
                    contents_page = requests.get(link)
                    contents_soup = BeautifulSoup(contents_page.content, 'html.parser')
                    title = contents_soup.find('h2').text
                    contents_div = contents_soup.find('div', attrs={'class': None, 'id': None})
                    paragraphs = contents_div.find_all('p', attrs={'class': None})
                    texts = [p.text for p in paragraphs]
                    text = texts[0]
                    date_div = contents_soup.find('p', class_='time')
                    date = date_div.find('span').text
                    news_by_topics[topics[i]].append((link, title, text, date))
                except:
                    continue
except:
    with open('telegram.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
        for topic, items in news_by_topics.items():
            for item in items:
                link, title, text, date = item
                csv_writer.writerow([date, topic, link, title, text])

with open('telegram.csv', 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
    for topic, items in news_by_topics.items():
        for item in items:
            link, title, text, date = item
            csv_writer.writerow([date, topic, link, title, text])