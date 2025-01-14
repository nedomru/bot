from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.user.inline import user_menu

user_router = Router()

async def is_user_in_channel(user_id: int, bot):
    channel_id = -1002068999312
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if sub.status != "left":
            return True
        else:
            await bot.send_message(chat_id=user_id, text='<b>Привет 👋</b>\n\n'
                                                         'Для доступа требуется подписка на канал <b>Не Дом.ру</b>\n\n'
                                                         '<b><a href="https://t.me/+F0O_FIydoKg2M2U6">Подписаться</a></b>\n\n'
                                                         'После подтверждения заявки вернись в бота и нажми /start', disable_web_page_preview=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return False


@user_router.message(CommandStart())
async def user_start(message: Message):
    if not await is_user_in_channel(message.from_user.id, bot=message.bot):
        return

    await message.answer("☎️ Главное меню <b>Не Дом.ру</b>\n\n"
                         "Я - бот-помощник проекта Не Дом.ру\n"
                         "Здесь ты найдешь расчет зарплаты, наш ВПН, и многое другое\n\n"
                         "<i>Используй кнопки ниже для управления меню</i>", reply_markup=user_menu())

@user_router.callback_query(F.data == "usermenu")
async def handle_menu(callback: CallbackQuery) -> None:
    """Главное меню"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    await callback.message.edit_text("☎️ Главное меню <b>Не Дом.ру</b>\n\n"
                         "Я - бот-помощник проекта Не Дом.ру\n"
                         "Здесь ты найдешь расчет ЗП, наш ВПН, и многое другое\n\n"
                         "<i>Используй кнопки ниже для управления мной</i>", reply_markup=user_menu())
    await callback.answer()

@user_router.callback_query(F.data == "usermenu_salary")
async def handle_salary(callback: CallbackQuery) -> None:
    """Меню зарплаты"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    await callback.answer()
