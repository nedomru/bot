from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def salary_count_type():
    buttons = [
        [
            InlineKeyboardButton(text="📊 Показатели", callback_data="usermenu_salary_type_percents"),
            InlineKeyboardButton(text="🌟 Общ. процент", callback_data="usermenu_salary_type_sum")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_position():
    buttons = [
        [
            InlineKeyboardButton(text="👶🏻 Спец.", callback_data="usermenu_salary_position_specialist"),
            InlineKeyboardButton(text="🔥 Ведущий Спец.", callback_data="usermenu_salary_position_lead_specialist")
        ],
        [
            InlineKeyboardButton(text="👑 Эксперт", callback_data="usermenu_salary_position_expert"),
        ],
        [
            InlineKeyboardButton(text="👨‍💻 РГ", callback_data="usermenu_salary_position_rg"),
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_aht():
    buttons = [
        [
            InlineKeyboardButton(text="0%", callback_data="aht_0"),
            InlineKeyboardButton(text="18%", callback_data="aht_18"),
            InlineKeyboardButton(text="28%", callback_data="aht_28")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_flr():
    buttons = [
        [
            InlineKeyboardButton(text="8%", callback_data="flr_8"),
            InlineKeyboardButton(text="13%", callback_data="flr_13"),
            InlineKeyboardButton(text="18%", callback_data="flr_18")
        ],
        [
            InlineKeyboardButton(text="21%", callback_data="flr_21"),
            InlineKeyboardButton(text="25%", callback_data="flr_25"),
            InlineKeyboardButton(text="30%", callback_data="flr_30")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_gok():
    buttons = [
        [
            InlineKeyboardButton(text="0%", callback_data="gok_0"),
            InlineKeyboardButton(text="5%", callback_data="gok_5"),
            InlineKeyboardButton(text="9%", callback_data="gok_9")
        ],
        [
            InlineKeyboardButton(text="12%", callback_data="gok_12"),
            InlineKeyboardButton(text="15%", callback_data="gok_15"),
            InlineKeyboardButton(text="17%", callback_data="gok_17")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_rate():
    buttons = [
        [
            InlineKeyboardButton(text="0%", callback_data="rate_0"),
            InlineKeyboardButton(text="5%", callback_data="rate_5"),
            InlineKeyboardButton(text="10%", callback_data="rate_10")
        ],
        [
            InlineKeyboardButton(text="15%", callback_data="rate_15"),
            InlineKeyboardButton(text="20%", callback_data="rate_20")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_tests():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="tests_yes"),
            InlineKeyboardButton(text="Нет", callback_data="tests_no")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_acknowledgments():
    buttons = [
        [
            InlineKeyboardButton(text="0%", callback_data="acknowledgments_0"),
            InlineKeyboardButton(text="3%", callback_data="acknowledgments_3"),
            InlineKeyboardButton(text="6%", callback_data="acknowledgments_6")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_mentor():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="mentor_yes"),
            InlineKeyboardButton(text="Нет", callback_data="mentor_no")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_mentor_type():
    buttons = [
        [
            InlineKeyboardButton(text="3D", callback_data="typementor_3d"),
            InlineKeyboardButton(text="Основной", callback_data="typementor_main"),
            InlineKeyboardButton(text="Общий", callback_data="typementor_general")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def salary_user_mentoring_days():
    buttons = [
        [
            InlineKeyboardButton(text="0", callback_data="daysmentoring_0"),
            InlineKeyboardButton(text="1", callback_data="daysmentoring_1"),
            InlineKeyboardButton(text="2", callback_data="daysmentoring_2"),
            InlineKeyboardButton(text="3", callback_data="daysmentoring_3")
        ],
        [
            InlineKeyboardButton(text="4", callback_data="daysmentoring_4"),
            InlineKeyboardButton(text="5", callback_data="daysmentoring_5"),
            InlineKeyboardButton(text="6", callback_data="daysmentoring_6"),
            InlineKeyboardButton(text="7", callback_data="daysmentoring_7")
        ],
        [
            InlineKeyboardButton(text="8", callback_data="daysmentoring_8"),
            InlineKeyboardButton(text="9", callback_data="daysmentoring_9"),
            InlineKeyboardButton(text="10", callback_data="daysmentoring_10"),
            InlineKeyboardButton(text="11", callback_data="daysmentoring_11")
        ],
        [
            InlineKeyboardButton(text="12", callback_data="daysmentoring_12"),
            InlineKeyboardButton(text="13", callback_data="daysmentoring_13"),
            InlineKeyboardButton(text="14", callback_data="daysmentoring_14"),
            InlineKeyboardButton(text="15", callback_data="daysmentoring_15"),
            InlineKeyboardButton(text="16", callback_data="daysmentoring_16")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
