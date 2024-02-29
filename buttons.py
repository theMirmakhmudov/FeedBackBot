from aiogram import types

btn = [
    [types.KeyboardButton(text="Feedback qoldirish")]

]
button = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)

contact_button = [
    [types.KeyboardButton(text="Contact ulashish", request_contact=True)]
]
contact = types.ReplyKeyboardMarkup(keyboard=contact_button, resize_keyboard=True)
