import json
import logging
from typing import Dict, Any

from aiogram import Router, F, Bot, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from algoliasearch.search.client import SearchClientSync

# from tgbot.misc.algolia import search

APP_ID = "DN83H0EFK4"
API_KEY = "26993d897f7166569aaa44ad941e0475"
INDEX_NAME = "flomaster-chrsnv"

inline_router = Router()


def search_documentation(query: str):
    client = SearchClientSync(APP_ID, API_KEY)
    try:
        results = client.search({
            "requests": [{
                "indexName": INDEX_NAME,
                "query": query
            }]
        })
        json_results = results.to_json()
        json_object = json.loads(json_results)
        return json_object["results"][0] if json_object["results"] else {}
    except Exception as e:
        logging.error(f"Algolia search error: {e}")
        return {}

async def is_user_in_channel(user_id: int, bot):
    channel_id = -1002068999312
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        logging.info(sub)
        return sub.status != "left"
    except Exception as e:
        print(f"Произошла ошибка при проверке подписки: {e}")
        return False


def search_algolia(query: str) -> Dict[str, Any]:
    client = SearchClientSync(APP_ID, API_KEY)
    try:
        results = client.search({
            "requests": [{
                "indexName": INDEX_NAME,
                "query": query
            }]
        })
        return json.loads(results.to_json())["results"][0]
    except Exception as e:
        logging.error(f"Algolia error: {e}")
        return {}

# === Inline Query обработчик ===
@inline_router.inline_query()
async def inline_search_handler(query: InlineQuery, bot: Bot):
    query_text = query.query.strip()
    if not query_text:
        await bot.answer_inline_query(query.id, results=[], cache_time=1)
        return

    results_data = search_algolia(query_text)
    hits = results_data.get("hits", [])
    results = []

    for i, hit in enumerate(hits[:10]):  # Ограничим до 10 результатов
        hierarchy = hit.get("hierarchy", {})
        title = " → ".join(filter(None, [hierarchy.get(f"lvl{j}") for j in range(7)])) or "Без названия"
        description = hit.get("url", "")
        message_url = hit.get("url", "")

        input_content = types.InputTextMessageContent(
            message_text=f"<b>Поиск по Фломастеру</b>\n\n"
                         f"🔎 Запрос: {query_text}\n"
                         f"🔗 Ссылка: <a href='{message_url}'>{title}</a>",
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        result = types.InlineQueryResultArticle(
            id=f"result_{i}",
            title=title,
            description=description,
            input_message_content=input_content,
            url=message_url,
            hide_url=False
        )

        results.append(result)

    await bot.answer_inline_query(query.id, results=results, cache_time=1)