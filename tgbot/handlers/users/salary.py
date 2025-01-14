import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.user.inline import to_home
from tgbot.keyboards.user.salary import salary_count_type, salary_user_position, salary_user_aht, salary_user_flr, \
    salary_user_gok, salary_user_rate, salary_user_tests, salary_user_acknowledgments, salary_user_mentor, \
    salary_user_mentor_type, salary_user_mentoring_days
from tgbot.misc.states import SalaryCountStates
from tgbot.misc.salary import salary_with_percents

user_salary_router = Router()


@user_salary_router.callback_query(F.data == "usermenu_salary")
async def start_count_salary(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await state.set_state(SalaryCountStates.COUNT_TYPE)

    await callback.message.edit_text("💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
                                     "В этом разделе ты можешь посчитать свои денежки\n\n"
                                     "Для начала выбери тип расчета:\n"
                                     "📊 Показатели - ручное заполнение показателей\n"
                                     "🌟 Общ. процент - ввод итогового процента премии <i>(это быстрее)</i>",
                                     reply_markup=salary_count_type())


@user_salary_router.callback_query(F.data.contains("usermenu_salary_type"))
@user_salary_router.message(SalaryCountStates.COUNT_TYPE)
async def process_salary_type(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    count_type = callback.data.split("_")[-1]
    await state.update_data(COUNT_TYPE=count_type)

    await state.set_state(SalaryCountStates.POSITION)
    if count_type == "sum":
        await callback.message.edit_text("💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
                                         "Хорошо, считаем по общему проценту премии\n\n"
                                         "💼 Теперь выбери ниже твою должность", reply_markup=salary_user_position())
    else:
        await callback.message.edit_text("💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
                                         "Хорошо, считаем процент каждого показателя отдельно\n\n"
                                         "💼 Теперь выбери ниже твою должность", reply_markup=salary_user_position())


@user_salary_router.callback_query(F.data.contains("position"))
@user_salary_router.message(SalaryCountStates.POSITION)
async def process_position(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(POSITION=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.HOURS_WORKED)
    bot_message = await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "Супер, должность выбрана!\n\n"
        "⏳ Введи в чат кол-во отработанных часов за месяц\n\n"
        "Часы можно найти в WFM\n"
        "<i><a href='https://i.imgur.com/qcE9TQA.png'>Пример на картинке</a></i>",
        reply_markup=to_home(),
        disable_web_page_preview=True)
    await state.update_data(LAST_BOT_MESSAGE_ID=bot_message.message_id)


@user_salary_router.message(SalaryCountStates.HOURS_WORKED)
async def process_hours_worked(message: Message, state: FSMContext) -> None:
    await state.update_data(HOURS_WORKED=message.text)
    user_data = await state.get_data()

    await message.delete()

    # Находим последнее сообщение бота и редактируем его
    bot_message = await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=user_data["LAST_BOT_MESSAGE_ID"],
        text="💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
             "Кол-во часов запомнил, давай продолжим\n\n" +
             ("🌟 Введи общий <b>процент премии</b>" if user_data[
                                                           "COUNT_TYPE"] == "sum" else "🚀 Выбери процент премии за <b>личную цель</b>\n\n"
                                                                                       "Найти его можно в Премиуме\n"
                                                                                       "<i><a href='https://i.imgur.com/L62rmBK.png'>Пример на картинке</a></i>"),
        reply_markup=to_home() if user_data["COUNT_TYPE"] == "sum" else salary_user_aht(),
        disable_web_page_preview=True
    )
    await state.update_data(LAST_BOT_MESSAGE_ID=bot_message.message_id)

    await state.set_state(
        SalaryCountStates.PREMIUM_PERCENT if user_data["COUNT_TYPE"] == "sum" else SalaryCountStates.AHT)


@user_salary_router.message(SalaryCountStates.PREMIUM_PERCENT)
async def process_premium_percent(message: Message, state: FSMContext) -> None:
    await state.update_data(PREMIUM_PERCENT=message.text)
    user_data = await state.get_data()

    # Удаляем сообщение пользователя
    await message.delete()

    if user_data["COUNT_TYPE"] == "sum":
        rate = None
        position_name = None
        match user_data["POSITION"]:
            case "nck1":
                rate = 156.7
                position_name = "Специалист НЦК1"
            case "nck1leading":
                rate = 164, 2
                position_name = "Ведущий специалист НЦК1"
            case "nck2":
                rate = 181
                position_name = "Специалист НЦК2"
            case "nck2":
                rate = 195.9
                position_name = "Ведущий специалист НЦК2"

        # Если был выбран общий процент премии, делаем расчет
        salary = await salary_with_percents(
            hourly_payment=rate,
            hours_worked=int(user_data["HOURS_WORKED"]),
            premium_percent=int(user_data["PREMIUM_PERCENT"]),
        )

        # Редактируем предыдущее сообщение с результатами
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=user_data["LAST_BOT_MESSAGE_ID"],
            text=f"""💸 <b>Не Дом.ру | Расчет ЗП</b>

<b>Показатели</b>
💼 <b>Должность</b>: {position_name}
🕖 <b>ЧТС</b>: {rate} руб/час
⏳ <b>Отработано</b>: {user_data["HOURS_WORKED"]} часов
🌟 <b>Процент премии</b>: {user_data["PREMIUM_PERCENT"]}%

<b>Зарплата</b>
Оклад составляет <b>{salary["hours_salary"]}</b> руб
Премия составляет <b>{salary["premium_salary"]}</b> руб

Общая сумма после вычета составляет <b>{salary["salary_sum"]}</b> руб

<blockquote expandable>
<b>Важно:</b>
1. В расчет берется часовая ставка по Перми
2. Коэффициент региона не учитывается
3. Налоги не учитываются
4. Я пока не умею считать ночные и праздничные часы

Разница в ЧТС нивелирует разницу в коэффициенте регионов
Коэфициент региона нивелируется налогами</blockquote>""",
            reply_markup=to_home()
        )
        await state.clear()
    else:
        await state.set_state(SalaryCountStates.AHT)
        # Если был выбран расчет через AHT, редактируем сообщение и ждем ответа на инлайн клавиатуру
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=user_data["LAST_BOT_MESSAGE_ID"],
            text="💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
                 "🚀 Выбери процент премии за <b>личную цель</b>\n\n"
                 "Найти его можно в Премиуме\n"
                 "<i><a href='https://i.imgur.com/L62rmBK.png'>Пример на картинке</a></i>",
            reply_markup=salary_user_aht(),
            disable_web_page_preview=True
        )


@user_salary_router.callback_query(F.data.contains("aht"))
@user_salary_router.message(SalaryCountStates.AHT)
async def process_aht(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(AHT=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.FLR)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "👽 Выбери процент премии за <b>FLR</b>\n\n"
        "Найти его можно в Премиуме\n"
        "<i><a href='https://i.imgur.com/lsEEoni.png'>Пример на картинке</a></i>",
        reply_markup=salary_user_flr(),
        disable_web_page_preview=True
    )


@user_salary_router.callback_query(F.data.contains("flr"))
@user_salary_router.message(SalaryCountStates.FLR)
async def process_flr(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(FLR=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.GOK)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "🤢 Выбери процент премии за <b>ГОК</b>\n\n"
        "Найти его можно в Премиуме\n"
        "<i><a href='https://i.imgur.com/S6cOdVK.png'>Пример на картинке</a></i>",
        reply_markup=salary_user_gok(),
        disable_web_page_preview=True
    )


@user_salary_router.callback_query(F.data.contains("gok"))
@user_salary_router.message(SalaryCountStates.GOK)
async def process_gok(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(GOK=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.CLIENT_RATING)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "⭐ Выбери процент премии за <b>оценку от клиента</b>\n\n"
        "Найти его можно в Премиуме\n"
        "<i><a href='https://i.imgur.com/LBKoWz8.png'>Пример на картинке</a></i>",
        reply_markup=salary_user_rate(),
        disable_web_page_preview=True
    )


@user_salary_router.callback_query(F.data.contains("rate"))
@user_salary_router.message(SalaryCountStates.CLIENT_RATING)
async def process_rate(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(CLIENT_RATING=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.TESTS)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "🧪 Прошел ли ты все <b>обязательные тесты</b>\n\n"
        "Найти тесты можно <a href='https://okc.ertelecom.ru/stats/testing/lk/profile'>тут</a>\n",
        reply_markup=salary_user_tests(),
    )


@user_salary_router.callback_query(F.data.contains("tests"))
@user_salary_router.message(SalaryCountStates.TESTS)
async def process_tests(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(TESTS=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.ACKNOWLEDGMENTS)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "🙏🏻 Выбери процент премии за <b>благодарности</b>\n\n"
        "1 благодарность - 3% премии\n"
        "Максимум благодарностей в месяц - 2\n\n"
        "Найти благодарности можно <a href='https://okc.ertelecom.ru/stats/thanks-appl/view/index'>тут</a>\n",
        reply_markup=salary_user_acknowledgments(),
    )


@user_salary_router.callback_query(F.data.contains("acknowledgments"))
@user_salary_router.message(SalaryCountStates.ACKNOWLEDGMENTS)
async def process_acknowledgments(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(ACKNOWLEDGMENTS=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.MENTOR)
    await callback.message.edit_text(
        "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
        "🎓 Ты <b>наставник</b>?\n",
        reply_markup=salary_user_mentor(),
    )


@user_salary_router.callback_query(F.data.startswith("mentor"))
@user_salary_router.message(SalaryCountStates.MENTOR)
async def process_mentoring(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(MENTOR=callback.data.split("_")[-1])

    if callback.data.split("_")[-1] == "yes":
        await state.set_state(SalaryCountStates.MENTOR_TYPE)
        await callback.message.edit_text(
            "💸 <b>Не Дом.ру | Расчет ЗП</b>\n\n"
            "🎓 Выбери тип наставничества",
            reply_markup=salary_user_mentor_type(),
        )
    else:
        user_data = await state.get_data()

        rate = None
        position_name = None
        match user_data["POSITION"]:
            case "nck1":
                rate = 156.7
                position_name = "Специалист НЦК1"
            case "nck1leading":
                rate = 164, 2
                position_name = "Ведущий специалист НЦК1"
            case "nck2":
                rate = 181
                position_name = "Специалист НЦК2"
            case "nck2":
                rate = 195.9
                position_name = "Ведущий специалист НЦК2"

        salary = await salary_with_percents(
            hourly_payment=rate,
            hours_worked=int(user_data["HOURS_WORKED"]),
            aht=int(user_data["AHT"]),
            flr=int(user_data["FLR"]),
            gok=int(user_data["GOK"]),
            client_rating=int(user_data["CLIENT_RATING"]),
            tests=user_data["TESTS"],
            acknowledgments=int(user_data["ACKNOWLEDGMENTS"]),
        )

        message = f"""💸 <b>Не Дом.ру | Расчет ЗП</b>

<b>Показатели</b>
💼 <b>Должность</b>: {position_name}
🕖 <b>ЧТС</b>: {rate} руб/час
⏳ <b>Отработано</b>: {user_data["HOURS_WORKED"]} часов
🚀 <b>Личная цель</b>: {user_data["AHT"]}%
👽 <b>FLR</b>: {user_data["FLR"]}%
🤢 <b>ГОК</b>: {user_data["GOK"]}%
⭐ <b>Оценка клиента</b>: {user_data["CLIENT_RATING"]}%
🧪 <b>Тесты</b>: {'Пройдены' if user_data["TESTS"] == "yes" else "Не пройдены"}
🙏🏻 <b>Благодарности</b>: {user_data["ACKNOWLEDGMENTS"]}%
🎓 <b>Наставничество</b>: Нет

<b>Зарплата</b>
Оклад составляет <b>{salary["hours_salary"]}</b> руб
Премия составляет <b>{salary["premium_salary"]}</b> руб

Общая сумма после вычета составляет <b>{salary["salary_sum"]}</b> руб

<blockquote expandable>
<b>Важно:</b>
1. В расчет берется часовая ставка по Перми
2. Коэффициент региона не учитывается
3. Налоги не учитываются
4. Я пока не умею считать ночные и праздничные часы

Разница в ЧТС нивелирует разницу в коэффициенте регионов
Коэфициент региона нивелируется налогами</blockquote>"""

        await callback.message.edit_text(message, reply_markup=to_home())
        await state.clear()


@user_salary_router.callback_query(F.data.contains("typementor"))
@user_salary_router.message(SalaryCountStates.MENTOR_TYPE)
async def process_mentoring_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(MENTOR_TYPE=callback.data.split("_")[-1])

    await state.set_state(SalaryCountStates.MENTOR_DAYS)
    await callback.message.edit_text(
        "🎓 Выбери кол-во дней наставничества в месяце",
        reply_markup=salary_user_mentoring_days(),
    )


@user_salary_router.callback_query(F.data.contains("daysmentoring"))
@user_salary_router.message(SalaryCountStates.MENTOR_DAYS)
async def process_mentoring_days(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(MENTOR_DAYS=callback.data.split("_")[-1])
    user_data = await state.get_data()

    rate = None
    position_name = None
    match user_data["POSITION"]:
        case "nck1":
            rate = 156.7
            position_name = "Специалист НЦК1"
        case "nck1leading":
            rate = 164, 2
            position_name = "Ведущий специалист НЦК1"
        case "nck2":
            rate = 181
            position_name = "Специалист НЦК2"
        case "nck2":
            rate = 195.9
            position_name = "Ведущий специалист НЦК2"

    salary = await salary_with_percents(
        hourly_payment=rate,
        hours_worked=int(user_data["HOURS_WORKED"]),
        aht=int(user_data["AHT"]),
        flr=int(user_data["FLR"]),
        gok=int(user_data["GOK"]),
        client_rating=int(user_data["CLIENT_RATING"]),
        tests=user_data["TESTS"],
        acknowledgments=int(user_data["ACKNOWLEDGMENTS"]),
        mentoring_type=user_data["MENTOR_TYPE"],
        mentoring_days=int(user_data["MENTOR_DAYS"]),
    )

    if user_data["MENTOR_TYPE"] == "3d":
        mentor_type = "3D"
    elif user_data["MENTOR_TYPE"] == "main":
        mentor_type = "Основной"
    else:
        mentor_type = "Общий"

    message = f"""💸 <b>Не Дом.ру | Расчет ЗП</b>

<b>Показатели</b>
💼 <b>Должность</b>: {position_name}
🕖 <b>ЧТС</b>: {rate} руб/час
⏳ <b>Отработано</b>: {user_data["HOURS_WORKED"]} часов
🚀 <b>AHT</b>: {user_data["AHT"]}%
👽 <b>FLR</b>: {user_data["FLR"]}%
🤢 <b>ГОК</b>: {user_data["GOK"]}%
⭐ <b>Оценка клиента</b>: {user_data["CLIENT_RATING"]}%
🧪 <b>Тесты</b>: {'Пройдены' if user_data["TESTS"] == "yes" else "Не пройдены"}
🙏🏻 <b>Благодарности</b>: {user_data["ACKNOWLEDGMENTS"]}%
🎓 <b>Наставничество</b>: {mentor_type}, {user_data["MENTOR_DAYS"]} дней

<b>Зарплата</b>
Оклад составляет <b>{salary["hours_salary"]}</b> руб
Премия составляет <b>{salary["premium_salary"]}</b> руб

Общая сумма после вычета составляет <b>{salary["salary_sum"]}</b> руб

<blockquote expandable>
<b>Важно:</b>
1. В расчет берется часовая ставка по Перми
2. Коэффициент региона не учитывается
3. Налоги не учитываются
4. Я пока не умею считать ночные и праздничные часы

Разница в ЧТС нивелирует разницу в коэффициенте регионов
Коэфициент региона нивелируется налогами</blockquote>"""
    await callback.message.edit_text(message, reply_markup=to_home())
    await state.clear()


@user_salary_router.callback_query(F.data == "purchases_sales")
async def my_orders(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вы открыли ваши часики!")
