from aiogram import Router, F
from aiogram.types import CallbackQuery

from tgbot.keyboards.user.inline import user_menu

user_vpn_router = Router()


@user_vpn_router.callback_query(F.data == "usermenu_vpn")
async def handle_menu_uservpn(callback: CallbackQuery) -> None:
    """Меню VPN"""
    await callback.message.edit_text("🛡️ Меню <b>Не Дом.ру | ВПН</b>\n\n"
                                     "<b>Доступные сервера</b>\n"
                                     "Австрия - <code>152.53.109.159</code>\n"
                                     "Швеция - <code>77.221.141.88</code>\n"
                                     "Германия - <code>150.241.99.169</code>\n\n"
                                     "<b>Технология</b>\n"
                                     "VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения\n"
                                     "Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы\n\n"
                                     "<b>Поддержка устройств</b>\n"
                                     "Поддерживаются все современные устройства, на которые есть приложения для подключения к VPN. Найти список доступных приложений можно на странице твоей подписки", reply_markup=user_menu())
    await callback.answer()
