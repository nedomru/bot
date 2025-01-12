from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Привет, админ!")

@admin_router.message(Command("kick"))
async def kick_user(message: Message):
    try:
        # Получаем user_id из аргумента функции
        user_id = int(message.text.split()[1])
        
        # Группы для кика
        groups = [-1002068999312, -1002186772934]
        
        results = []
        for group_id in groups:
            try:
                # Attempt to kick user from each group
                await message.bot.ban_chat_member(
                    chat_id=group_id,
                    user_id=user_id
                )
                results.append(f"✅ Юзер успешно исключен из {group_id}")
            except Exception as e:
                results.append(f"❌ Не удалось кикнуть юзера из {group_id}: {str(e)}")
        
        # Отправка репорта
        await message.reply("\n".join(results))
        
    except (IndexError, ValueError):
        await message.reply("❌ Некорректный формат. Используй: /kick USER_ID")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {str(e)}")