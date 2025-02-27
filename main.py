# uvicorn main:app --reload
import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


from tg_bots.close_work_day.start import start_bot
@app.on_event("startup")
async def start_telegram_bot():
    # Запускаем Telegram-клиента в фоновом режиме
    asyncio.create_task(start_bot())
    print("Telegram bot is running...")

from tg_bots.close_work_day.chat_mute_control import chat_mute_control
@app.on_event("startup")
async def close_chat_bot():
    asyncio.create_task(chat_mute_control())
    
# from tg_bots.close_work_day.get_group_id import get_group_id
# @app.on_event("startup")
# async def start_get_group_id():
#     asyncio.create_task(get_group_id())

# WIEV
@app.get("/")
def read_root():
    return "ok"