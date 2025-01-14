from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def user_menu():
    buttons = [
        [
            InlineKeyboardButton(text="💵 Расчет ЗП", callback_data="usermenu_salary"),
        ],
        [
            InlineKeyboardButton(text='🤝 Группа', url="https://t.me/+6aXdfP0eGIsyYWQ6"),
            InlineKeyboardButton(text='📺 Канал', url="https://t.me/+F0O_FIydoKg2M2U6")
        ],
        [
            InlineKeyboardButton(text='✏️ Фломастер', web_app=WebAppInfo(url=f'https://flomaster.chrsnv.ru/')),
            InlineKeyboardButton(text='📖 Гайдмастер', web_app=WebAppInfo(url=f'https://guides.chrsnv.ru/'))
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard

def to_home():
    buttons = [
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard