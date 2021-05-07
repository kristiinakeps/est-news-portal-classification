import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'authority': 'epl.delfi.ee',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-US,en;q=0.9,sv;q=0.8',
    'cookie': 'cstp=1; cX_S=kj7237izjr9vmefh; cX_P=kj7237j4ii8ria99; cX_G=cx^%^3A1481kaqyzdazi3u36creqx9jy0^%^3Afg20aiyu1g7y; _ga=GA1.2.2040377803.1616946796; _edt=0:kmtcdgl6:k7QuZV3qUFUprOzreAN2BQklpANjE34P; dcid=1675586872,1,1648482796,1616946796,9b3d8e9ecfdffc9f04c44aac446a6da8; _hjTLDTest=1; _hjid=a038d240-2f81-4d6e-90c9-24353531a481; __utma=78189697.2040377803.1616946796.1617515183.1617515183.1; __utmc=78189697; __utmz=78189697.1617515183.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); evid_0020=cx:1481kaqyzdazi3u36creqx9jy0:fg20aiyu1g7y; evid_00XX=cx:1481kaqyzdazi3u36creqx9jy0:fg20aiyu1g7y; cX_cint_set=1; __gfp_64b=1gDHeKP3OXXGG6cz7dsmHK0tOtUHw8._8GoRLUcA0iL.a7^|1598970184; loginApiToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaWQiOjEwMjIzODksImlzcyI6ImxvZ2luLWFwaSIsImV4cCI6MTY1MDgxNzM2MSwiaWF0IjoxNjE5MjgxMzYxfQ.T-b-C_Cj7OyCMsSdyk3gtGkelh_rDXgIS3t81vlxxYM; idp=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaWQiOjEwMjIzODksImlzcyI6ImxvZ2luLWFwaSIsImV4cCI6MTY1MDgxNzM2MSwiaWF0IjoxNjE5MjgxMzYxfQ.T-b-C_Cj7OyCMsSdyk3gtGkelh_rDXgIS3t81vlxxYM; cp_user_package=64930263; cp_user_package_t=1619411341344; _gid=GA1.2.940482182.1619411342; _edid=0:kny3p8m3:EicbKXcjlrkGJA0DcEJ7BC_nR564AiFH; _hjAbsoluteSessionInProgress=1',
}

URL = 'https://epl.delfi.ee/kategooria/'
article_URL = 'https://epl.delfi.ee'
topics = ['uudised', 'arvamus', 'kultuur', 'sport', 'valismaa', 'lp', 'arileht']
codes = ['67583608', '67583634', '67583652', '67583654', '67583610', '67583658', '67583628']
pages = [121, 121, 121, 121, 121, 121, 121]
news_by_topics = {}

try:
    for i in range(0, len(topics)):
        news_by_topics[topics[i]] = []
        print(topics[i])
        for j in range(1, pages[i] + 1):
            print(j)
            page_url = '' if j == 1 else '?page=' + str(j)
            page = requests.get(URL + codes[i] + '/' + topics[i] + page_url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            news_links = soup.find_all('h5', class_='C-headline-title')
            for news in news_links:
                try:
                    a = news.find('a')
                    link = a['href']
                    title = a.text
                    if not link.startswith('https://'):
                        link = article_URL + link
                    contents_page = requests.get(link, headers=headers)
                    contents_soup = BeautifulSoup(contents_page.content, 'html.parser')
                    date = contents_soup.find('div', class_='C-article-info__publish-date').text
                    paragraphs = contents_soup.find_all('p')
                    texts = [p.text for p in paragraphs]
                    text = '\n'.join(texts)
                    news_by_topics[topics[i]].append((link, title, text, date))
                except:
                    continue
except:
    with open('paevaleht.csv', 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
        for topic, items in news_by_topics.items():
            for item in items:
                link, title, text, date = item
                csv_writer.writerow([date, topic, link, title, text])

with open('paevaleht.csv', 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['kpv', 'teema', 'link', 'pealkiri', 'sisu'])
    for topic, items in news_by_topics.items():
        for item in items:
            link, title, text, date = item
            csv_writer.writerow([date, topic, link, title, text])