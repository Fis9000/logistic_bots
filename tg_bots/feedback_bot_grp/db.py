import sqlite3

async def create_db():
    # Подключение к базе данных (файл будет создан, если его нет)
    conn = sqlite3.connect('my_database.db')

    # Создание курсора
    cursor = conn.cursor()

    # Создание таблицы с двумя столбцами: Key и Value
    cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                    (Key TEXT PRIMARY KEY, Value TEXT)''')

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения
    conn.close()

    print("База данных и таблица созданы успешно!")

async def add_db_info():
    # Подключение к базе данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Добавление данных
    cursor.execute("INSERT INTO my_table (Key, Value) VALUES (?, ?)", ('key11', 'value11'))
    cursor.execute("INSERT INTO my_table (Key, Value) VALUES (?, ?)", ('key22', 'value22'))

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения
    conn.close()

    print("Данные добавлены успешно!")