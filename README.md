# Запуск
Для запуска проекта:
1. Клонируй проект:

`git clone https://devops.chrsnv.ru/nedomru/bot.git`

2. Сделай копию файла переменных

`cp .env.dist .env`

3. Заполни обязательные переменные

- BOT_TOKEN = токен бота от @BotFather
- ADMINS = id администраторов
- USE_REDIS = использовать REDIS

4. Запусти проект

`docker compose up -d`