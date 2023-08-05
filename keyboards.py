from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboards = [
    KeyboardButton('Достопримечательности'),
    KeyboardButton('Информация'),
    KeyboardButton('Отели'),
    KeyboardButton('Поесть'),
    KeyboardButton('Новости'),
    KeyboardButton('Ваканции'),
    KeyboardButton('Реклама'),
    KeyboardButton('Верификация')
]

verify_keyboards = [
    KeyboardButton('Отправить номер', request_contact=True),
    KeyboardButton('Отправить локацию', request_location=True),
    KeyboardButton('Назад')
]

start_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*start_keyboards)

verify_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*verify_keyboards)

admin_keyboards = [
    InlineKeyboardButton('Добавить достопримечательность', callback_data="add_admin_sights"),
    InlineKeyboardButton('Удалить достопримечательность', callback_data="delete_admin_sights"),
    InlineKeyboardButton('Сделать рассылку', callback_data="make_newsletter"),
    InlineKeyboardButton('Выдать админку', callback_data="add_new_admin"),
    InlineKeyboardButton('Удалить админку', callback_data="delete_admin")
]

admin_button = InlineKeyboardMarkup(row_width=2).add(*admin_keyboards)