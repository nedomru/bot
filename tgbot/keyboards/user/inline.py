from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def user_menu():
    buttons = [
        [
            InlineKeyboardButton(text="💵 Расчет ЗП", callback_data="usermenu_salary"),
            InlineKeyboardButton(text="🌐 VPN", callback_data="usermenu_vpn"),
        ],
        [
            InlineKeyboardButton(text='Фломастер', web_app=WebAppInfo(url=f'https://flomaster.chrsnv.ru/')),
            InlineKeyboardButton(text='Гайдмастер', web_app=WebAppInfo(url=f'https://guides.chrsnv.ru/'))
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
