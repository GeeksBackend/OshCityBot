from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, aioschedule, requests, logging, asyncio

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}. {message.chat.id} Введите комманду /spam чтобы спамить сообщениями")

async def get_spam():
    await bot.send_message(-891592921, "SPAMMM BOT")

async def send_notification_lesson_09():
    await bot.send_message(-891592921, "Добрый день, дорогие студенты! 🌟 Хотим вам напомнить, что сегодня у вас запланирован урок в 18:00. Пожалуйста, приходите вовремя, чтобы не опаздывать! 👍")

async def get_btc_price():
    url = "https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT"
    response = requests.get(url).json()
    await bot.send_message(-891592921, f"Текущий курс биткоина: {response['price']}$")

async def scheduler():
    # aioschedule.every(0.5).seconds.do(get_spam)
    # aioschedule.every().wednesday.at("18:45").do(send_notification_lesson_09)
    aioschedule.every(1).seconds.do(get_btc_price)
    while True:
        await aioschedule.run_pending()

async def on_startup(hello):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)