from aiogram import Router, F
from aiogram.types import CallbackQuery

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import admin_vpn_menu

admin_vpn_router = Router()
admin_vpn_router.message.filter(AdminFilter())


@admin_vpn_router.callback_query(F.data == "adminmenu_vpn")
async def handle_vpn_menu(callback: CallbackQuery) -> None:
    """Меню VPN"""
    await callback.message.edit_text("🛡️ Меню <b>Не Дом.ру | ВПН</b>", reply_markup=admin_vpn_menu())
    await callback.answer()

@admin_vpn_router.callback_query(F.data == "adminmenu_vpn_serverstatus")
async def handle_vpn_serverstatus(callback: CallbackQuery) -> None:
    """Статус сервера"""
    await callback.answer()

@admin_vpn_router.callback_query(F.data == "adminmenu_vpn_users")
async def handle_vpn_users(callback: CallbackQuery) -> None:
    """Пользователи VPN"""
    await callback.answer()

@admin_vpn_router.callback_query(F.data == "adminmenu_vpn_nodes")
async def handle_vpn_nodes(callback: CallbackQuery) -> None:
    """Ноды"""
    await callback.answer()

@admin_vpn_router.callback_query(F.data == "adminmenu_vpn_restartxray")
async def handle_vpn_restartxray(callback: CallbackQuery) -> None:
    """Рестарт хрея"""
    await callback.answer()

@admin_vpn_router.callback_query(F.data == "adminmenu_vpn_restartxray")
async def handle_vpn_restartxray(callback: CallbackQuery) -> None:
    """Рестарт хрея"""
    await callback.answer()