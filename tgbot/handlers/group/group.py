import logging

from aiogram import Router, types

group_router = Router()

GROUP_ID = -1002477224245
SOURCE_TOPIC_ID = 4

@group_router.message()
async def handle_messages(message: types.Message):
    """Forward messages from source topic to destination topic"""
    # Check if message is from the correct group and topic
    if (message.chat.id == GROUP_ID and 
        message.message_thread_id == SOURCE_TOPIC_ID):
        try:
            # Forward based on message type
            if message:
                await message.bot.forward_message(chat_id=GROUP_ID, from_chat_id=GROUP_ID, message_id=message.message_id)
            
            logging.info(
                f"Forwarded message from topic {SOURCE_TOPIC_ID} to main topic"
            )
            
        except Exception as e:
            logging.error(f"Error forwarding message: {e}")