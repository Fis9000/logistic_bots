from telegram import Bot
from telegram.error import TelegramError
import time
from globals import GlobalConfig
from tg_bots.actions.send_message import send_message_to_group
from tg_bots.feedback_bot_grp.json_handler import load_key_responses  # Изменено на импорт из json_handler

TELEGRAM_TOKEN = GlobalConfig.feedback_tg_bot_token
GROUP_ID = GlobalConfig.feedback_tg_bot_group_id

# Входящие сообщения
async def incoming_messages():
    bot = Bot(token=TELEGRAM_TOKEN)
    last_update_id = None

    # Очищаем очередь обновлений при старте
    updates = await bot.get_updates()
    if updates:
        last_update_id = updates[-1].update_id + 1
        await bot.get_updates(offset=last_update_id)  # Очищаем очередь

    while True:
        try:
            # Получаем обновления с offset, чтобы избежать повторений
            updates = await bot.get_updates(offset=last_update_id)

            # Если обновлений нет, ждем и продолжаем
            if not updates:
                time.sleep(1)
                continue

            # Загружаем ключевые слова и ответы из JSON-файла
            key_responses = await load_key_responses()

            for update in updates:
                if update.message:
                    user_message = update.message.text
                    user_name = update.message.from_user.first_name
                    user_message_id = update.message.id

                    # Логи
                    print(f"{user_name} написал - '{user_message}'")
                    
                    # Проверяем, что сообщение содержит текст
                    if user_message is not None:
                        # Ключевые слова
                        message_text = user_message.lower()
                        for keyword, response in key_responses.items():
                            if keyword == message_text:
                                await send_message_to_group(TELEGRAM_TOKEN, update.message.chat_id, response)
                    # Обновляем last_update_id для получения только новых сообщений
                    last_update_id = update.update_id + 1

            time.sleep(1)  # задержка
        except TelegramError as e:
            print(f"Ошибка при получении обновлений: {e}")     
                   
async def feedback_bot_grp_start_bot():
    await incoming_messages()