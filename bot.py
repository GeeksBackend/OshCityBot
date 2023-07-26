from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, time, logging

from keyboards import start_button
from database import connection, cursor

load_dotenv('.env')

bot = Bot(token=str(os.environ.get('token')))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()
    print(result)
    if result == []:
        cursor.execute(f"""INSERT INTO users VALUES ({message.from_user.id}, '{message.from_user.username}',
                    '{message.from_user.first_name}', '{message.from_user.last_name}', '{time.ctime()}');""")
        cursor.connection.commit()
    await message.answer(f"Здравствуйте, {message.from_user.full_name}\nЯ вам помогу узнать наш город Ош в мельчайших подробностях\nЧто вас интересует на данный момент?", reply_markup=start_button)

@dp.message_handler(commands='mailing')
async def mailing(message:types.Message):
    cursor.execute("SELECT id FROM users;")
    users_id = cursor.fetchall()
    print(users_id[0])
    for i in range(len(users_id)):
        for id in users_id[i]:
            await bot.send_message(chat_id=id, text='Реклама от бота')
    await message.answer("Рассыка окончена")

executor.start_polling(dp, skip_updates=True)