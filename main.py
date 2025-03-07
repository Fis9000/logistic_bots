# uvicorn main:app --reload
import asyncio
from fastapi import FastAPI
from globals import GlobalConfig

app = FastAPI()

print("START")

# # Бот обратной связи
from tg_bots.feedback_bot_grp.start import feedback_bot_grp_start_bot
@app.on_event("startup")
async def start_close_work_day_bot():
    asyncio.create_task(feedback_bot_grp_start_bot())
    print("Telegram bot | close_work_day | is running...")

# # Бот обратной связи (закрытие/открытие чата)
from tg_bots.feedback_bot_grp.chat_mute_control import chat_mute_control
@app.on_event("startup")
async def start_chat_mute_control():
    asyncio.create_task(chat_mute_control())

# Бот редакоирования ключевых слов для бота обратной связи
from tg_bots.feedback_bot_grp.edit_key_bot_grp.start import edit_key_bot_grp_start_bot
@app.on_event("startup")
async def start_main():
    asyncio.create_task(edit_key_bot_grp_start_bot())

# Скачать бд
from sqllite_download import router as sqllite_download_router
app.include_router(sqllite_download_router, prefix="/download")

# from tg_bots.feedback_bot_grp.db import add_db_info
# @app.on_event("startup")
# async def start_add_db_info():
#     asyncio.create_task(add_db_info())

# GROUP ID (подставить нужный токен бота)
# from tg_bots.feedback_bot_grp.get_group_id import get_group_id
# @app.on_event("startup")
# async def start_get_group_id():
#     asyncio.create_task(get_group_id(GlobalConfig.edit_feedback_tg_bot_token))

###

# Бот оплаты
from tg_bots.pay_bot.start import pay_bot_start_bot
@app.on_event("startup")
async def start_pay_bot_start_bot():
    asyncio.create_task(pay_bot_start_bot())

#
@app.get("/")
def read_root():
    return "ok"