from fastapi import APIRouter, FastAPI, Response
from fastapi.responses import FileResponse
import os

router = APIRouter()
app = FastAPI()

@router.get("/download_my_database")
async def download_db():
    file_path = "my_database.db"
    
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    # Возвращаем файл для скачивания
    return FileResponse(file_path, filename="my_database.db", media_type="application/octet-stream")
