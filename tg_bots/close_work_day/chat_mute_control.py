import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import ChatPermissions
from tg_bots.close_work_day.send_message import send_message_to_group
from globals import GlobalConfig

# Вкл/Выкл возможности отправки сообщений пользователями (в отдельнеом потоке)

TELEGRAM_TOKEN = GlobalConfig.tg_bot_token
GROUP_ID = GlobalConfig.tg_bot_group_id

close_message = (
    "🔒 Чат закрыт! Можно писать только с 09:00 до 18:00.\n"
    "Для подачи запросов используйте специальный раздел: [Ссылка на раздел]"
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

        close_time = current_time.replace(hour=18, minute=00, second=0, microsecond=0)
        open_time = current_time.replace(hour=9, minute=00, second=0, microsecond=0)

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
            await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, close_message)
            await close_chat()
        else:
            await send_message_to_group(TELEGRAM_TOKEN, GROUP_ID, open_message)
            await open_chat()

