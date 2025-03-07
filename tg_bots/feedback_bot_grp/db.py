# import sqlite3

# async def create_db():
#     # Подключение к базе данных (файл будет создан, если его нет)
#     conn = sqlite3.connect('my_database.db')

#     # Создание курсора
#     cursor = conn.cursor()

#     # Создание таблицы с двумя столбцами: Key и Value
#     cursor.execute('''CREATE TABLE IF NOT EXISTS feedback_bot_grp_keys
#                     (Key TEXT PRIMARY KEY, Value TEXT)''')

#     # Сохранение изменений
#     conn.commit()

#     # Закрытие соединения
#     conn.close()

#     print("База данных и таблица созданы успешно!")

# async def add_db_info(_key, _value):
#     # Подключение к базе данных
#     conn = sqlite3.connect('my_database.db')
#     cursor = conn.cursor()

#     # Добавление данных
#     # cursor.execute("INSERT INTO my_table (Key, Value) VALUES (?, ?)", ('key11', 'value11'))
#     cursor.execute("INSERT INTO feedback_bot_grp_keys (Key, Value) VALUES (?, ?)", (_key, _value))

#     # Сохранение изменений
#     conn.commit()

#     # Закрытие соединения
#     conn.close()

#     print("Данные добавлены успешно!")

# # Передаем словарь в группу
# async def load_key_responses():
#     # Подключение к базе данных
#     conn = sqlite3.connect('my_database.db')
#     cursor = conn.cursor()

#     # Загрузка данных из таблицы
#     cursor.execute("SELECT Key, Value FROM feedback_bot_grp_keys")
#     rows = cursor.fetchall()

#     # Закрытие соединения
#     conn.close()

#     # Преобразование данных в словарь
#     key_responses = {key: value for key, value in rows}
#     return key_responses