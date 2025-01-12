from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# This is a simple keyboard, that contains 2 buttons
def accept_to_channel(user_id):
    buttons = [
        [
            InlineKeyboardButton(text="✔️ Принять",
                                 callback_data="accept_channel"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data="deny_channel"),
        ],
        [
            InlineKeyboardButton(text="✉️ Написать", url=f"https://t.me/{user_id}"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard

def leaved_user(user_id):
    buttons = [
        [
            InlineKeyboardButton(text="✉️ Написать", url=f"https://t.me/{user_id}"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard