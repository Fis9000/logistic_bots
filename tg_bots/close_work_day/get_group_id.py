from telegram import Bot
from telegram.error import TelegramError
from globals import GlobalConfig

# Получение id группы, в которой находится бот

TELEGRAM_TOKEN = GlobalConfig.tg_bot_token

async def get_group_id():
    bot = Bot(token=TELEGRAM_TOKEN)

    try:
        # Очищаем старые обновления
        await bot.get_updates(offset=-1)
        print("Очередь обновлений очищена. Отправьте сообщение в группу и попробуйте снова.")

        # Получаем новые обновления после очистки
        updates = await bot.get_updates(timeout=10)

        if updates:
            for update in updates:
                print(update.to_dict())  # Диагностика

                if update.message:
                    print(f"ID вашей группы: {update.message.chat.id}")
                elif update.channel_post:
                    print(f"ID супергруппы/канала: {update.channel_post.chat.id}")
                elif update.my_chat_member:
                    print(f"ID при изменении членства: {update.my_chat_member.chat.id}")
                else:
                    print("Обновление без сообщения, пропускаем.")
        else:
            print("Нет новых обновлений. Убедитесь, что отправили новое сообщение в группу.")
    except TelegramError as e:
        print(f"Ошибка Telegram API: {e}")
