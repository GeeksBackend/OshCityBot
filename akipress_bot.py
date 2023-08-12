from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests, logging, os

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Привет {message.from_user.full_name}')

@dp.message_handler(commands='news')
async def send_parsing_news(message:types.Message):
    await message.reply("Начинаю парсинг новости с сайта...")
    url = 'https://akipress.org/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find_all('a', class_='newslink')
    n = 0
    for news_text in news:
        n += 1
        await message.answer(f"{n}) {news_text.text}")

executor.start_polling(dp, skip_updates=True)