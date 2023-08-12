from bs4 import BeautifulSoup
import requests

url = 'https://akipress.org/'
response = requests.get(url=url)
print(response)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)
news = soup.find_all('a', class_='newslink')
# print(news)
"""Задание сделать так чтобы новости были пронумерованы и также были 
записаны в отдельный txt файл в названием news.txt (дается 10 минут) 19:49"""
n = 0
for news_text in news:
    n += 1
    # print(news_text.text)
    with open('news.txt', 'a+', encoding='utf-8') as f:
        f.write(f"{n}) {news_text.text}\n")