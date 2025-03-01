# uvicorn main:app --reload
import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

print("START")

from tg_bots.close_work_day.start import close_work_day_start_bot
@app.on_event("startup")
async def start_close_work_day_bot():
    asyncio.create_task(close_work_day_start_bot())
    print("Telegram bot | close_work_day | is running...")

from tg_bots.close_work_day.chat_mute_control import chat_mute_control
@app.on_event("startup")
async def start_chat_mute_control():
    asyncio.create_task(chat_mute_control())
    
# from tg_bots.close_work_day.get_group_id import get_group_id
# @app.on_event("startup")
# async def start_get_group_id():
#     asyncio.create_task(get_group_id())

from tg_bots.pay_bot.start import pay_bot_start_bot
@app.on_event("startup")
async def start_pay_bot_start_bot():
    asyncio.create_task(pay_bot_start_bot())

#
@app.get("/")
def read_root():
    return "ok"