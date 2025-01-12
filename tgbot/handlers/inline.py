from aiogram import Router, F, Bot, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import aiohttp
import json

inline_router = Router()


async def fetch_mna_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://helper.chrsnv.ru/api/mna.json') as response:
            data = await response.json()
            return data['mna']


@inline_router.inline_query()
async def handle_inline_query(query: InlineQuery):
    try:
        mna_data = await fetch_mna_data()
        results = []

        # Filter data if query is provided
        search_query = query.query.lower()
        filtered_data = [
            item for item in mna_data
            if search_query in item['name'].lower() or
               search_query in item['authorization'].lower() or
               search_query in item['connection'].lower()
        ] if search_query else mna_data

        # Create results
        for idx, item in enumerate(filtered_data):
            message_text = (
                f"Провайдер *{item['name']}*\n\n"
                f"🔐 Тип авторизации: {item['authorization']}\n"
                f"🔌 Тип подключения: {item['connection']}\n"
                f"🔗 [Провайдер в БЗ]({item['link']})"
            )

            results.append(
                InlineQueryResultArticle(
                    id=str(idx),
                    title=item['name'],
                    description=f"Авторизация: {item['authorization']} | Подключение: {item['connection']}",
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    ),
                )
            )

        # If no results found
        if not results:
            results.append(
                InlineQueryResultArticle(
                    id="not_found",
                    title="Ничего не найдено",
                    description="Попробуйте изменить поисковый запрос",
                    input_message_content=InputTextMessageContent(
                        message_text="К сожалению, по вашему запросу ничего не найдено."
                    )
                )
            )

        await query.answer(
            results=results,
            cache_time=300,  # Cache for 5 minutes
            is_personal=True
        )

    except Exception as e:
        # Handle errors
        error_result = InlineQueryResultArticle(
            id="error",
            title="Произошла ошибка",
            description="Не удалось загрузить данные",
            input_message_content=InputTextMessageContent(
                message_text="К сожалению, произошла ошибка при загрузке данных. Попробуйте позже."
            )
        )
        await query.answer(
            results=[error_result],
            cache_time=5
        )