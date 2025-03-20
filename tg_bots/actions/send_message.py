from telegram import Bot, InputFile
from telegram.error import TelegramError

# Функция отправки сообщений и изображений в группу
async def send_message_to_group(_tg_token, _group_id, _text, image_path=None):
    bot = Bot(token=_tg_token)
    try:
        if image_path:  # Если указан путь к изображению
            with open(image_path, "rb") as photo:
                await bot.send_photo(chat_id=_group_id, photo=photo, caption=_text)
        else:
            await bot.send_message(chat_id=_group_id, text=_text)
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения: {e}")
