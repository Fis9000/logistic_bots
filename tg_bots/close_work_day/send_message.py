from telegram import Bot, Update
from telegram.error import TelegramError

# Функция отправки сообщений

async def send_message_to_group(_tg_token, _group_id, _text):
    bot = Bot(token=_tg_token)
    try:
        # Отправляем сообщение в группу
        await bot.send_message(chat_id=_group_id, text=_text)
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения: {e}")
