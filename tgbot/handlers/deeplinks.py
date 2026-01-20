"""Deep link handlers for authorization via session links."""

import os
import logging

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery

from infrastructure.database.models.users import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

deeplink_router = Router()


@deeplink_router.message(CommandStart())
async def process_deeplink_start(
    message: Message, command: CommandObject, user, config, **kwargs
):
    """
    Process /start command with session ID (deeplink).
    Format: /start <session_id>
    """
    # Check if command has arguments (session_id)
    if not command.args:
        # No session ID provided - let the user router handle it
        return

    session_id = command.args
    await _handle_authorization_request(message, session_id, user, config)


async def _handle_authorization_request(
    message: Message, session_id: str, user, config
):
    """
    Handle authorization request from deeplink.
    Checks user access and authorizes the session via API.
    """
    # Check if user has access
    if not user.access:
        await message.answer(
            "❌ <b>Доступ запрещен</b>\n\n"
            "У вас нет доступа к системе. Обратитесь к администратору."
        )
        return

    # Get user data from Telegram
    tg_user = message.from_user

    # Check if user was just created (has default settings)
    is_new_user = user.settings == DEFAULT_SETTINGS

    # Show authorization message with button
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔑 Авторизоваться", callback_data=f"auth_{session_id}"
                )
            ]
        ]
    )

    welcome_text = (
        f"🔐 <b>Запрос на авторизацию</b>\n\nПривет, {tg_user.first_name}!\n\n"
    )

    if is_new_user:
        welcome_text += "✨ Вы были автоматически зарегистрированы в системе.\n\n"

    welcome_text += "Используй кнопку ниже для подтверждения входа в Хелпер"

    await message.answer(welcome_text, reply_markup=keyboard)


@deeplink_router.callback_query(lambda c: c.data and c.data.startswith("auth_"))
async def process_authorization_callback(
    callback: CallbackQuery, user, config, **kwargs
):
    """
    Handle the authorize button click - authorize the session via API.
    """
    await callback.answer()

    # Extract session ID from callback data
    session_id = callback.data.replace("auth_", "")

    # Check if user has access
    if not user.access:
        await callback.message.edit_text(
            "❌ <b>Доступ запрещен</b>\n\n"
            "У вас нет доступа к системе. Обратитесь к администратору."
        )
        return

    # Get user data from Telegram
    tg_user = callback.from_user
    user_data = {
        "id": tg_user.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
        "language_code": tg_user.language_code,
    }

    # Call the API to authorize the session
    import aiohttp

    # Get API base URL from config
    api_base = (
        config.misc.api_base
        if hasattr(config, "misc")
        else os.getenv("API_BASE", "http://localhost:4321")
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{api_base}/api/auth/authorize",
                json={"sessionId": session_id, "userData": user_data},
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        await callback.message.edit_text(
                            "✅ <b>Успешная авторизация!</b>\n\n"
                            "Вход был успешно выполнен. Вы можете закрыть это сообщение."
                        )
                    else:
                        await callback.message.edit_text(
                            f"❌ <b>Ошибка авторизации</b>\n\n"
                            f"{data.get('error', 'Неизвестная ошибка')}"
                        )
                elif response.status == 404:
                    await callback.message.edit_text(
                        "❌ <b>Сессия не найдена</b>\n\n"
                        "Сессия истекла или не существует. Попробуйте запросить новую ссылку."
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"API error: {response.status} - {error_text}")
                    await callback.message.edit_text(
                        "❌ <b>Ошибка авторизации</b>\n\nПопробуйте позже."
                    )
    except aiohttp.ClientError as e:
        logger.error(f"Client error during authorization: {e}")
        await callback.message.edit_text(
            "❌ <b>Ошибка соединения</b>\n\n"
            "Не удалось подключиться к серверу авторизации. Попробуйте позже."
        )
    except Exception as e:
        logger.error(f"Unexpected error during authorization: {e}")
        await callback.message.edit_text(
            "❌ <b>Неизвестная ошибка</b>\n\n"
            "Произошла непредвиденная ошибка. Попробуйте позже."
        )
