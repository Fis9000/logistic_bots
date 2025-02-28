from datetime import datetime, timedelta, timezone
import pytz
from telegram import Bot, Update
from telegram.error import TelegramError
import time
from globals import GlobalConfig
from tg_bots.close_work_day.send_message import send_message_to_group

TELEGRAM_TOKEN = GlobalConfig.tg_bot_token
GROUP_ID = GlobalConfig.tg_bot_group_id

# Список ключевых слов и ответов
key_responses = {
    "привет": "Привет!",
    "помощь": "Чем Вам помочь?"
}

# Входящие
async def incoming_messages():
    bot = Bot(token=TELEGRAM_TOKEN)
    last_update_id = None

    while True:
        try:
            # Получаем обновления с offset, чтобы избежать повторений
            updates = await bot.get_updates(offset=last_update_id)

            for update in updates:
                if update.message:
                    user_message = update.message.text
                    user_name = update.message.from_user.first_name

                    # Логи
                    print(f"{user_name} написал - '{user_message}'")

                    # Ключевые слова
                    message_text = user_message.lower()
                    for keyword, response in key_responses.items():
                        if keyword in message_text:
                            await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, response)

                    # Обновляем last_update_id для получения только новых сообщений
                    last_update_id = update.update_id + 1

            time.sleep(1)  # задержка
        except TelegramError as e:
            print(f"Ошибка при получении обновлений: {e}")

async def close_work_day_start_bot():
    await incoming_messages()
