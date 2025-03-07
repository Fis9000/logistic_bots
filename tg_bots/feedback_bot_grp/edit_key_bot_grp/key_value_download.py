from fastapi import APIRouter, FastAPI, Response
from fastapi.responses import FileResponse
import os

router = APIRouter()
app = FastAPI()

@router.get("/download_key_value")
async def download_db():
    file_path = "key_value.json"
    
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    # Возвращаем файл для скачивания
    return FileResponse(file_path, filename="key_value.json", media_type="application/octet-stream")
