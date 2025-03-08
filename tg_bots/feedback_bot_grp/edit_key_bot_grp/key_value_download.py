from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, FastAPI, Response
from fastapi.responses import FileResponse
import os
import zipfile
from io import BytesIO

router = APIRouter()
app = FastAPI()

@router.get("/download_key_value")
async def download_files():
    moscow_tz = timezone(timedelta(hours=3))
    date_time = datetime.now(moscow_tz).strftime("%d-%m-%Y %H:%M:%S")

    file_paths = [
        "tg_bots/feedback_bot_grp/edit_key_bot_grp/key_value.json",
        "tg_bots/feedback_bot_grp/edit_key_bot_grp/logs.txt"
    ]

    # Проверяем, существуют ли файлы
    for file_path in file_paths:
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} not found"}

    # Создаем ZIP-архив в памяти
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))

    # Перемещаем указатель в начало буфера
    zip_buffer.seek(0)

    # Возвращаем ZIP-архив для скачивания
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=edit_key_bot_grp " + date_time + ".zip"}
    )