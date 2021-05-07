import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://uueduudised.ee/rubriik/'
topics = ['arvamus', 'eesti', 'maailm', 'majandus', 'varia', 'video']
pages = [70, 117, 74, 9, 7, 6]
news_by_topics = {}

try:
    for i in range(len(topics)):
        news_by_topics[topics[i]] = []
        print(topics[i])
        for j in range(1, pages[i] + 1):
            print(j)
            page_url = '/' if j == 1 else '/page/' + str(j) + '/'
            page = requests.get(URL + topics[i] + page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            news_links = soup.find_all('div', class_='news_box_item ajax_item clearfix')
            for news in news_links:
                try:
                    a = news.find('a', class_='news_box_link')
                    date = news.find('span', attrs={'style': 'font-size:12px;color:#444;'}).text
                    link = a['href']
                    title = a.text
                    contents_page = requests.get(link)
                    contents_soup = BeautifulSoup(contents_page.content, 'html.parser')
                    contents_div = contents_soup.find('div', class_='blog_post_content post_content')
                    paragraphs = contents_div.find_all('p')
                    texts = [p.text for p in paragraphs]
                    text = '\n'.join(texts)
                    news_by_topics[topics[i]].append((link, title, text, date))
                except:
                    continue
except Exception as e:
    print(e)
    with open('uued_uudised.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
        for topic, items in news_by_topics.items():
            for item in items:
                link, title, text, date = item
                csv_writer.writerow([date, topic, link, title, text])

with open('uued_uudised.csv', 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
    for topic, items in news_by_topics.items():
        for item in items:
            link, title, text, date = item
            csv_writer.writerow([date, topic, link, title, text])