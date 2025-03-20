import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import ChatPermissions
from tg_bots.actions.send_message import send_message_to_group
from globals import GlobalConfig

# Вкл/Выкл возможности отправки сообщений пользователями (в отдельнеом потоке)

TELEGRAM_TOKEN = GlobalConfig.feedback_tg_bot_token
GROUP_ID = GlobalConfig.feedback_tg_bot_group_id

CLOSE_IMAGE_PATH = "tg_bots/feedback_bot_grp/img1.jpg"

close_message = (
    "Коллеги, добрый вечер! С 18:00 до 09:00 по Московскому времени закрыта возможность отправлять сообщения в эту группу.\n\nЕсли у вас остались вопросы, которые вы бы хотели задать - вам нужно перейти в бот, где вы берете заказы (у кого этого бота нет - переходим в бот регистрации и проходим ее, @Gpm_registration_bot)\n"
    "Внутри бота вы вызываете меню, далее нажимаете на 'мои данные', после - кнопка 'Написать вопрос\пожелание\предложение'.\nВводите свой вопрос и отправляете.\n\n" 
    "Всем хорошего вечера!"
)
open_message = "✅ Чат открыт!"

bot = Bot(token=TELEGRAM_TOKEN)

async def close_chat():
    permissions = ChatPermissions(can_send_messages=False)
    await bot.set_chat_permissions(chat_id=GROUP_ID, permissions=permissions)

async def open_chat():
    permissions = ChatPermissions(can_send_messages=True)
    await bot.set_chat_permissions(chat_id=GROUP_ID, permissions=permissions)

async def chat_mute_control():
    while True:
        moscow_tz_offset = timedelta(hours=3)
        current_time = datetime.utcnow() + moscow_tz_offset

        close_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)
        open_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)

        if current_time >= close_time:
            close_time += timedelta(days=1)
        if current_time >= open_time:
            open_time += timedelta(days=1)

        next_event, action = (
            (close_time, "close") if close_time < open_time else (open_time, "open")
        )

        time_to_sleep = (next_event - current_time).total_seconds()
        print(f"🕒 Следующее действие ({'закрытие' if action == 'close' else 'открытие'}) в {next_event}. "
              f"Ожидание {time_to_sleep // 3600:.0f}ч {time_to_sleep % 3600 // 60:.0f}м.")

        await asyncio.sleep(time_to_sleep)

        if action == "close":
            await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, close_message, CLOSE_IMAGE_PATH)
            await close_chat()
        else:
            await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, open_message)
            await open_chat()

