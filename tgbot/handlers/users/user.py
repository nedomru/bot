import os
import logging

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.dialogs.states.user import UserSG
from infrastructure.database.models.users import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def user_start(
    message: Message,
    command: CommandObject,
    dialog_manager: DialogManager,
    user,
    config,
    **kwargs,
):
    """Handle /start command - either deeplink authorization or default menu."""
    # Check if command has arguments (deeplink session_id)
    if command.args:
        session_id = command.args
        await _handle_deeplink_authorization(message, session_id, user, config)
    else:
        # No arguments - start the default user dialog
        await dialog_manager.start(UserSG.main, mode=StartMode.RESET_STACK)


async def _handle_deeplink_authorization(
    message: Message, session_id: str, user, config
):
    """Handle authorization request from deeplink - direct API call."""
    import aiohttp

    # Check if user has access
    if not user.access:
        await message.answer(
            "❌ <b>Доступ запрещен</b>\n\n"
            "У вас нет доступа к системе. Обратитесь к администратору."
        )
        return

    # Get user data from Telegram
    tg_user = message.from_user
    user_data = {
        "id": tg_user.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
        "language_code": tg_user.language_code,
    }

    # Check if user was just created (has default settings)
    is_new_user = user.settings == DEFAULT_SETTINGS

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
                        success_text = "✅ <b>Успешная авторизация!</b>\n\n"
                        success_text += f"Привет, {tg_user.first_name}!\n\n"
                        if is_new_user:
                            success_text += "✨ Вы были автоматически зарегистрированы в системе.\n\n"
                        success_text += "Вход был успешно выполнен. Вы можете закрыть это сообщение."
                        await message.answer(success_text)
                    else:
                        await message.answer(
                            f"❌ <b>Ошибка авторизации</b>\n\n"
                            f"{data.get('error', 'Неизвестная ошибка')}"
                        )
                elif response.status == 404:
                    await message.answer(
                        "❌ <b>Сессия не найдена</b>\n\n"
                        "Сессия истекла или не существует. Попробуйте запросить новую ссылку."
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"API error: {response.status} - {error_text}")
                    await message.answer(
                        "❌ <b>Ошибка авторизации</b>\n\nПопробуйте позже."
                    )
    except aiohttp.ClientError as e:
        logger.error(f"Client error during authorization: {e}")
        await message.answer(
            "❌ <b>Ошибка соединения</b>\n\n"
            "Не удалось подключиться к серверу авторизации. Попробуйте позже."
        )
    except Exception as e:
        logger.error(f"Unexpected error during authorization: {e}")
        await message.answer(
            "❌ <b>Неизвестная ошибка</b>\n\n"
            "Произошла непредвиденная ошибка. Попробуйте позже."
        )


