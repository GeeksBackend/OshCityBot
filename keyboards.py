from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_keyboards = [
    KeyboardButton('Backend 🏗️'),
    KeyboardButton('Frontend 👷'),
    KeyboardButton('Ux/Ui Дизайн 🌈'),
    KeyboardButton('Аndroid 🤖'),
    KeyboardButton('iOS 📱🖥️'),
]

start_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*start_keyboards)
