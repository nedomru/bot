from typing import Callable, Dict, Any, Awaitable

import logging
from aiogram import BaseMiddleware
from aiogram.types import Message


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

        try:
            # Check if user is in the channel
            await bot.get_chat_member(
                chat_id=self.CHANNEL_ID, user_id=event.from_user.id
            )
        except Exception as e:
            logger.error(f"Channel check failed for user {event.from_user.id}: {e}")
            await event.answer(
                "Для доступа требуется подписка на <a href='https://t.me/+jH1mblw0ytcwOWUy'>канал</a>."
            )
            return None

        try:
            # Check if user is in the group
            await bot.get_chat_member(chat_id=self.GROUP_ID, user_id=event.from_user.id)
        except Exception as e:
            logger.error(f"Group check failed for user {event.from_user.id}: {e}")
            await event.answer(
                "Для доступа требуется нахождение в <a href='https://t.me/+2vVZ0vXJiWFkOWZi'>чате</a>."
            )
            return None

        return await handler(event, data)
