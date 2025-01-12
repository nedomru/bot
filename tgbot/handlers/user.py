from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import user_menu

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer("☎️ Главное меню <b>Не Дом.ру</b>", reply_markup=user_menu())

@user_router.callback_query(F.data == "usermenu")
async def handle_menu(callback: CallbackQuery) -> None:
    """Главное меню"""
    await callback.message.edit_text("☎️ Главное меню <b>Не Дом.ру</b>", reply_markup=user_menu())
    await callback.answer()

@user_router.callback_query(F.data == "usermenu_salary")
async def handle_salary(callback: CallbackQuery) -> None:
    """Меню зарплаты"""
    await callback.answer()

@user_router.callback_query(F.data == "usermenu_vpn")
async def handle_vpn(callback: CallbackQuery) -> None:
    """Меню зарплаты"""
    await callback.answer()