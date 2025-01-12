from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import CallbackQuery, ChatJoinRequest, ChatMemberUpdated
from aiogram import Bot
import logging
from typing import Dict

from datetime import datetime, timedelta

from tgbot.keyboards.inline import accept_to_channel, leaved_user

channel_router = Router()

# Храним входящие запросы
# Формат: {message_id: (chat_id, user_id, timestamp)}
pending_requests: Dict[int, tuple[int, int, datetime]] = {}


@channel_router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest, bot: Bot) -> None:
    """Обрабатываем входящие запросы на вход."""
    user = request.from_user
    chat_id = request.chat.id
    
    # Получаем инфо о пригласительной ссылке
    invite_info = ""
    if request.invite_link:
        invite_info = f"\nПришел по ссылке: <i>{request.invite_link.name if request.invite_link.name else request.invite_link.invite_link}</i>"

    try:
        # Отправка уведомления админу
        admin_msg = await bot.send_message(
            chat_id=6486127400,
            text=f"<b>Вход в канал</b>\nПользователь {user.username} (ID: {user.id}) оставил запрос на вход в канал{invite_info}",
            reply_markup=accept_to_channel(user_id=user.username)
        )

        pending_requests[admin_msg.message_id] = (chat_id, user.id, datetime.now())

        # Чистим старые запросы (старше 24 часов)
        current_time = datetime.now()
        expired_messages = [
            msg_id for msg_id, (_, _, timestamp) in pending_requests.items()
            if current_time - timestamp > timedelta(hours=24)
        ]
        for msg_id in expired_messages:
            pending_requests.pop(msg_id)

        logging.info(f"Stored join request from {user.username} (ID: {user.id})")

    except Exception as e:
        logging.error(f"Error handling join request: {e}")

@channel_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated, bot: Bot):
    # Отправка уведомления админу
    await bot.send_message(
        chat_id=6486127400,
        text=f"<b>Выход из канала</b>\nПользователь {event.from_user.username} (ID: {event.from_user.id}) покинул канал",
        reply_markup=leaved_user(user_id=event.from_user.username)
    )

@channel_router.callback_query(F.data == "accept_channel")
async def handle_accept_channel(callback: CallbackQuery, bot: Bot) -> None:
    """Подтверждение заявки на вход в канал"""
    try:
        if callback.message.message_id not in pending_requests:
            await callback.answer("Запрос устарел или уже обработан", show_alert=True)
            return

        chat_id, user_id, _ = pending_requests[callback.message.message_id]

        # Подтверждение заявки на вход
        try:
            await bot.approve_chat_join_request(
                chat_id=chat_id,
                user_id=user_id
            )
            logging.info(f"Approved join request for user ID: {user_id}")
        except Exception as e:
            logging.error(f"Failed to approve join request: {e}")
            await callback.answer("Ошибка при одобрении запроса", show_alert=True)
            return

        # Удаление обработанной заявки
        pending_requests.pop(callback.message.message_id)

        message_text = callback.message.text
        await callback.message.edit_text(
            f"{message_text}\n\n✅ Принят администратором {callback.from_user.username}",
            reply_markup=None
        )

        # Уведомление пользователя о подтверждении заявки
        try:
            await bot.send_message(
                chat_id=user_id,
                text="✅ Ваша заявка на вступление в канал была одобрена!"
            )
        except Exception as e:
            logging.error(f"Failed to send approval message to user: {e}")

        await callback.answer("Пользователь успешно принят")

    except Exception as e:
        logging.error(f"Error handling accept channel callback: {e}")
        await callback.answer("Произошла ошибка при обработке запроса", show_alert=True)


@channel_router.callback_query(F.data == "deny_channel")
async def handle_deny_channel(callback: CallbackQuery, bot: Bot) -> None:
    """Отмена заявки на вход в канал"""
    try:
        if callback.message.message_id not in pending_requests:
            await callback.answer("Запрос устарел или уже обработан", show_alert=True)
            return

        chat_id, user_id, _ = pending_requests[callback.message.message_id]

        # Отмена заявки
        try:
            await bot.decline_chat_join_request(
                chat_id=chat_id,
                user_id=user_id
            )
            logging.info(f"Declined join request for user ID: {user_id}")
        except Exception as e:
            logging.error(f"Failed to decline join request: {e}")
            await callback.answer("Ошибка при отклонении запроса", show_alert=True)
            return

        # Удаление обработанной заявки
        pending_requests.pop(callback.message.message_id)

        message_text = callback.message.text
        await callback.message.edit_text(
            f"{message_text}\n\n❌ Отклонен администратором {callback.from_user.username}",
            reply_markup=None
        )

        # Уведомление пользователя об отмене заявки
        try:
            await bot.send_message(
                chat_id=user_id,
                text="❌ Ваша заявка на вступление в канал была отклонена."
            )
        except Exception as e:
            logging.error(f"Failed to send denial message to user: {e}")

        await callback.answer("Пользователь отклонен")

    except Exception as e:
        logging.error(f"Error handling deny channel callback: {e}")
        await callback.answer("Произошла ошибка при обработке запроса", show_alert=True)