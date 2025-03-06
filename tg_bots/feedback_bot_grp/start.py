from datetime import timedelta, timezone
from telegram import Bot, Update
from telegram.error import TelegramError
import time
from globals import GlobalConfig
from tg_bots.actions.send_message import send_message_to_group
from tg_bots.feedback_bot_grp.db import load_key_responses

TELEGRAM_TOKEN = GlobalConfig.feedback_tg_bot_token
GROUP_ID = GlobalConfig.feedback_tg_bot_group_id

# Список ключевых слов и ответов
# key_responses = {
#     "привет": "Привет!",
#     "помощь": "Чем Вам помочь?",
# }

# Входящие
async def incoming_messages():
    bot = Bot(token=TELEGRAM_TOKEN)
    last_update_id = None

    
    while True:
        try:
            # Получаем обновления с offset, чтобы избежать повторений
            updates = await bot.get_updates(offset=last_update_id)

            key_responses = await load_key_responses()

            for update in updates:
                if update.message:
                    user_message = update.message.text
                    user_name = update.message.from_user.first_name

                    # Логи
                    print(f"{user_name} написал - '{user_message}'")
                    
                    # Проверяем, что сообщение содержит текст
                    if user_message is not None:
                        # Ключевые слова
                        message_text = user_message.lower()
                        for keyword, response in key_responses.items():
                            if keyword == message_text:
                                await send_message_to_group(TELEGRAM_TOKEN, update.message.chat_id, response)
                                # await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, response)
                    # Обновляем last_update_id для получения только новых сообщений
                    last_update_id = update.update_id + 1

            time.sleep(1)  # задержка
        except TelegramError as e:
            print(f"Ошибка при получении обновлений: {e}")

async def feedback_bot_grp_start_bot():
    await incoming_messages()