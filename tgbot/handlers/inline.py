from aiogram import Router, F, Bot, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import requests
import json
from functools import lru_cache

inline_router = Router()


@lru_cache(maxsize=1)
def fetch_mna_data():
    response = requests.get('https://helper.chrsnv.ru/api/mna.json', verify=False)
    return response.json()['mna']


@inline_router.inline_query()
async def handle_inline_query(query: InlineQuery):
    try:
        mna_data = fetch_mna_data()  # This is now a synchronous call
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
                f"📡 *{item['name']}*\n\n"
                f"🔐 Авторизация: {item['authorization']}\n"
                f"🔌 Подключение: {item['connection']}\n"
                f"🔗 [Подробнее]({item['link']})"
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
            cache_time=300,
            is_personal=True
        )

    except Exception as e:
        print(f"Error: {e}")  # Add debug logging
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