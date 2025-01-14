from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Принятие в канал
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


# Сообщение ливнувшему юзеру
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


# Админ-меню
def admin_menu():
    buttons = [
        [
            InlineKeyboardButton(text="👨‍👦‍👦 Пользователи", callback_data="adminmenu_users"),
            InlineKeyboardButton(text="🌐 VPN", callback_data="adminmenu_vpn"),
        ],
        [
            InlineKeyboardButton(text="💵 Расчет ЗП", callback_data="usermenu_salary"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def admin_vpn_menu():
    buttons = [
        [
            InlineKeyboardButton(text="📊 Статус сервера", callback_data="adminmenu_vpn_serverstatus")
        ],
        [
            InlineKeyboardButton(text="👨‍👦‍👦 Пользователи", callback_data="adminmenu_vpn_users"),
            InlineKeyboardButton(text="🌐 Ноды", callback_data="adminmenu_vpn_nodes"),
        ],
        [
            InlineKeyboardButton(text="🌀 Ребут ядра", callback_data="adminmenu_vpn_restartxray"),
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="adminmenu"),
        ],

    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard