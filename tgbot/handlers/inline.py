import logging

from aiogram import Router, F, Bot, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

inline_router = Router()

# Локальный список MnA
MNA_DATA = [
    {
        "name": "Interzet",
        "authorization": "IPoE Static",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3289"
    },
    {
        "name": "Тура-Telecom",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3280"
    },
    {
        "name": "Ярославль Телесеть (ЯТС)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3136"
    },
    {
        "name": "Иркнет",
        "authorization": "PPPoE",
        "connection": "ADSL / GPON / FTTH",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3192"
    },
    {
        "name": "Контакт (Тула)",
        "authorization": "PPPoE",
        "connection": "ADSL",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3282"
    },
    {
        "name": "Коламбия Телеком",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet / ADSL",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2761"
    },
    {
        "name": "Телемир (Липецк)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3191"
    },
    {
        "name": "Акадо (СПБ)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3291"
    },
    {
        "name": "БКС (Брянск)",
        "authorization": "DHCP mac+vlan / DHCP",
        "connection": "Ethernet / PON",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2760"
    },
    {
        "name": "Инфоцентр (Сосновый бор)",
        "authorization": "IPoE Static",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3285"
    },
    {
        "name": "Конвекс/ТКС (ЕКБ)",
        "authorization": "IPoE Static / PPTP (общежития)",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2769"
    },
    {
        "name": "Дельта-Телеком",
        "authorization": "PPPoE",
        "connection": "ADSL",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3106"
    },
    {
        "name": "Мегаполис-Телеком",
        "authorization": "PPPoE",
        "connection": "PON",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3189"
    },
    {
        "name": "СибТелеКом (СТК)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet / ADSL",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3121"
    },
    {
        "name": "Westcall / N-Link (Рязань)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet / ADSL / PON",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3288"
    },
    {
        "name": "Акадо (ЕКБ)",
        "authorization": "L2TP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2768"
    },
    {
        "name": "Сатурн (Пермь)",
        "authorization": "PPPoE",
        "connection": "FTTH",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/6528"
    },
    {
        "name": "Westcall (СПб)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3286"
    },
    {
        "name": "Кредолинк (СПб)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3283"
    },
    {
        "name": "MSNet (СПБ)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3287"
    },
    {
        "name": "Стрела (Димитровград)",
        "authorization": "DHCP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3172"
    },
    {
        "name": "С-Телеком МСК (Самолет)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3238"
    },
    {
        "name": "Дианэт (Барнаул и область)",
        "authorization": "PPPoE / L2TP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2646"
    },
    {
        "name": "НТС (Томск)",
        "authorization": "IPoE DHCP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3648"
    },
    {
        "name": "Кроникс/Rinet",
        "authorization": "DHCP / DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3246/page/3"
    }
]


async def is_user_in_channel(user_id: int, bot):
    channel_id = -1002068999312
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        logging.info(sub)
        return sub.status != "left"
    except Exception as e:
        print(f"Произошла ошибка при проверке подписки: {e}")
        return False


@inline_router.inline_query()
async def handle_inline_query(query: InlineQuery, bot: Bot):
    try:
        if not await is_user_in_channel(query.from_user.id, bot):
            subscription_text = (
                "❗️ Для использования бота требуется подписка на канал\n\n"
                "📢 <b>Не Дом.ру</b>\n"
                "🔗 https://t.me/+F0O_FIydoKg2M2U6\n\n"
                "После подписки вернись и попробуй еще раз"
            )

            return await query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="subscribe_required",
                        title="Требуется подписка на канал",
                        description="Подпишись на канал Не Дом.ру для доступа",
                        input_message_content=InputTextMessageContent(
                            message_text=subscription_text,
                            parse_mode="HTML",
                            disable_web_page_preview=True
                        ),
                        thumb_url="https://img.icons8.com/color/48/000000/subscription.png",
                    )
                ],
                cache_time=5,
                is_personal=True
            )

        results = []
        # Rest of your code remains the same...
        search_query = query.query.lower()
        filtered_data = [
            item for item in MNA_DATA
            if search_query in item['name'].lower() or
               search_query in item['authorization'].lower() or
               search_query in item['connection'].lower()
        ] if search_query else MNA_DATA

        # Create results
        for idx, item in enumerate(filtered_data):
            message_text = (
                f"📡 *{item['name']}*\n\n"
                f"🔐 Авторизация: {item['authorization']}\n"
                f"🔌 Подключение: {item['connection']}\n\n"
                f"[Подробнее в БЗ]({item['link']})"
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
        print(f"Error in inline query: {e}")
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
