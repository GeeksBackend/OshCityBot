from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import os, time, logging

from keyboards import start_button, verify_button
from database import cursor

load_dotenv('.env')

bot = Bot(token=str(os.environ.get('token')))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
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

class MailingState(StatesGroup):
    text = State()

@dp.message_handler(commands='id')
async def get_my_id(message:types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")

@dp.message_handler(commands='mailing')
async def get_mailing_text(message:types.Message):
    if message.from_user.id in [731982105, 234234234]:
        await message.reply("Введите текст для рассылки")
        await MailingState.text.set()
    else:
        await message.reply("У вас нет прав для данного действия")

@dp.message_handler(state=MailingState.text)
async def mailing(message:types.Message, state:FSMContext):
    cursor.execute("SELECT id FROM users;")
    users_id = cursor.fetchall()
    print(users_id[0])
    for i in range(len(users_id)):
        for id in users_id[i]:
            await bot.send_message(chat_id=id, text=message.text)
    await message.answer("Рассыка окончена")
    await state.finish()

@dp.message_handler(text='Информация')
async def information(message:types.Message):
    await message.answer("""Ош — город республиканского подчинения в Киргизии, административный центр Ошской области.
Ош — второй по численности населения город Киргизии после Бишкека, крупнейший город юга страны, официально именуемый «южной столицей». 
18 декабря 2018 года город Ош объявлен Культурной столицей тюркского мира на 2019 год.""")

class SightsState(StatesGroup):
    title = State()
    description = State()
    location = State()
    longitude = State()
    latitude = State()

@dp.message_handler(commands='add_sights')
async def get_sights_title(message:types.Message):
    if message.from_user.id in [731982105]:
        await message.answer("Введите заголовок")
        await SightsState.title.set()
    else:
        await message.reply("У вас нет прав для данного действия")

@dp.message_handler(state=SightsState.title)
async def get_sights_description(message:types.Message, state:FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание")
    await SightsState.description.set()

@dp.message_handler(state=SightsState.description)
async def get_sights_address(message:types.Message, state:FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите адрес")
    await SightsState.location.set()

@dp.message_handler(state=SightsState.location)
async def get_sights_longitude(message:types.Message, state:FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Введите долготу")
    await SightsState.longitude.set()

@dp.message_handler(state=SightsState.longitude)
async def get_sights_latitude(message:types.Message, state:FSMContext):
    await state.update_data(longitude=message.text)
    await message.answer("Введите широту")
    await SightsState.latitude.set()

@dp.message_handler(state=SightsState.latitude)
async def add_sights_to_db(message:types.Message, state:FSMContext):
    await state.update_data(latitude=message.text)
    result = await storage.get_data(user=message.from_user.id)
    print(result)
    await message.answer("Добавляю в базу данных")
    cursor.execute(f"""INSERT INTO sights VALUES ('{result['title']}',
                   '{result['description']}', '{result['location']}',
                   '{result['longitude']}', '{result['latitude']}');""")
    cursor.connection.commit()
    await message.answer("Добавили в базу данных")
    await state.finish()

async def get_dynamic_buttons():
    buttons = []
    cursor.execute("SELECT title FROM sights;")
    items = cursor.fetchall()
    for i in range(len(items)):
        for item in items[i]:
            buttons.append(types.KeyboardButton(item))
    buttons.append(types.KeyboardButton("Назад"))
    return buttons

class GetSightsState(StatesGroup):
    title = State()

@dp.message_handler(text='Достопримечательности')
async def show_sights(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dynamic_buttons = await get_dynamic_buttons()
    keyboard.add(*dynamic_buttons)
    await message.answer("Вот наши достопримечательности:", reply_markup=keyboard)
    await GetSightsState.title.set()

@dp.message_handler(state=GetSightsState.title)
async def get_sigths_title_user(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await start(message)
    cursor.execute(f"SELECT * FROM sights WHERE title = '{message.text}';")
    result = cursor.fetchall()
    await message.reply(f"""{result[0][0]}
{result[0][1]}
Адрес: {result[0][2]}""")
    await message.reply_location(result[0][3], result[0][4])

@dp.message_handler(text="Верификация")
async def verify(message:types.Message):
    await message.answer("Пройдите верификацию аккаунта", reply_markup=verify_button)

@dp.message_handler(text="Назад")
async def back_start(message:types.Message):
    await start(message)

executor.start_polling(dp, skip_updates=True)