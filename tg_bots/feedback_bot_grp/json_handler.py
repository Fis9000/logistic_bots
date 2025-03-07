import json
import os

# Путь к JSON-файлу
JSON_FILE_PATH = 'data.json'

# Функция для загрузки данных из JSON-файла
async def load_key_responses():
    if not os.path.exists(JSON_FILE_PATH):
        return {}
    
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

# Функция для добавления данных в JSON-файл
async def add_db_info(key, value):
    data = await load_key_responses()
    data[key] = value
    
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Функция для удаления данных из JSON-файла
async def remove_db_info(key):
    data = await load_key_responses()
    if key in data:
        del data[key]
        
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    return False