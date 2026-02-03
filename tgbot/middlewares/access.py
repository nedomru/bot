from typing import Callable, Dict, Any, Awaitable

import logging
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


logger = logging.getLogger(__name__)


class AccessMiddleware(BaseMiddleware):
    CHANNEL_ID = -1002068999312
    GROUP_ID = -1003653519335

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        bot = data["bot"]
        user_id = event.from_user.id

        logger.info(f"AccessMiddleware: Checking access for user {user_id}")

        # Valid statuses: member, administrator, creator
        VALID_STATUSES = {"member", "administrator", "creator"}

        try:
            # Check if user is in the channel
            member = await bot.get_chat_member(
                chat_id=self.CHANNEL_ID, user_id=user_id
            )
            logger.info(f"User {user_id} channel status: {member.status}")

            if member.status not in VALID_STATUSES:
                logger.warning(f"User {user_id} not in channel (status: {member.status})")
                await event.answer(
                    "Для доступа требуется подписка на <a href='https://t.me/+jH1mblw0ytcwOWUy'>канал</a>."
                )
                return
        except TelegramBadRequest as e:
            logger.warning(f"User {user_id} not in channel: {e}")
            await event.answer(
                "Для доступа требуется подписка на <a href='https://t.me/+jH1mblw0ytcwOWUy'>канал</a>."
            )
            return
        except Exception as e:
            logger.error(f"Unexpected error checking channel for user {user_id}: {e}")
            await event.answer("Ошибка проверки доступа к каналу")
            return

        try:
            # Check if user is in the group
            member = await bot.get_chat_member(chat_id=self.GROUP_ID, user_id=user_id)
            logger.info(f"User {user_id} group status: {member.status}")

            if member.status not in VALID_STATUSES:
                logger.warning(f"User {user_id} not in group (status: {member.status})")
                await event.answer(
                    "Для доступа требуется нахождение в <a href='https://t.me/+2vVZ0vXJiWFkOWZi'>чате</a>."
                )
                return
        except TelegramBadRequest as e:
            logger.warning(f"User {user_id} not in group: {e}")
            await event.answer(
                "Для доступа требуется нахождение в <a href='https://t.me/+2vVZ0vXJiWFkOWZi'>чате</a>."
            )
            return
        except Exception as e:
            logger.error(f"Unexpected error checking group for user {user_id}: {e}")
            await event.answer("Ошибка проверки доступа к чату")
            return

        logger.info(f"AccessMiddleware: User {user_id} passed all checks")
        return await handler(event, data)
