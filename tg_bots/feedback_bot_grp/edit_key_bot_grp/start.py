from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from tg_bots.feedback_bot_grp.db import add_db_info, load_key_responses
from globals import GlobalConfig

# Токен бота
TELEGRAM_TOKEN = GlobalConfig.edit_feedback_tg_bot_token
GROUP_ID = GlobalConfig.edit_feedback_tg_bot_group_id

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Класс для хранения состояний
class Form(StatesGroup):
    waiting_for_keyword = State()
    waiting_for_value = State()

inline_keyboard = [
    [InlineKeyboardButton(text=("Добавить ключевое слово"), callback_data = "add_key_value_btn")],
    [InlineKeyboardButton(text=("Удалить ключевое слово"), callback_data = "del_key_value_btn")],
    [InlineKeyboardButton(text=("Список ключевых слов"), callback_data = "all_key_value_btn")]
    ]
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Функция для отправки reply-кнопок в группу
async def send_reply_buttons(chat_id, _text):
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ключевое слово"), KeyboardButton(text="Удалить ключевое слово"), KeyboardButton(text="Список ключевых слов")]
        ],
        resize_keyboard=True
    )
    await bot.send_message(chat_id, _text, reply_markup=reply_keyboard)

@dp.message(lambda message: message.new_chat_members)
async def on_new_member(message: types.Message):
    for user in message.new_chat_members:
        user_name = user.first_name  # Получаем имя пользователя
        if user.last_name:
            user_name += f" {user.last_name}"
    await send_reply_buttons(message.chat.id, "Новый пользователь: " + user_name + "")  # Отправляем reply-кнопки каждому новому пользователю
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    # Если эта кнопка нажата во время процесса добавления key-value
    data = await state.get_data()
    if "keyword" in data:
        await message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
        await state.clear()  # Сбрасываем состояние

    # menu = InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton(text=("Добавить ключевое слово"), callback_data = "add_key_value_btn")],
    #     [InlineKeyboardButton(text=("Удалить ключевое слово"), callback_data = "del_key_value_btn")],
    #     [InlineKeyboardButton(text=("Список ключевых слов"), callback_data = "all_key_value_btn")],
    # ])
    menu = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await send_reply_buttons(message.chat.id, "Здесь Вы можете добавить или удалить ключевые слова для бота обатной связи")  # Отправляем reply-кнопки при /start
    await message.answer("Выберите действие:", reply_markup=menu)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик reply-кнопок
@dp.message(lambda message: message.text in ["Добавить ключевое слово", "Удалить ключевое слово", "Список ключевых слов"])
async def process_reply_buttons(message: types.Message, state: FSMContext):
    if message.text == "Добавить ключевое слово":  # Нажатие на кнопку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value_null")],
        ])
        await message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key

    # if message.text == "Удалить ключевое слово":  # Нажатие на кнопку
    #     key_responses = await load_key_responses()  # Загружаем ключевые слова из базы данных
    #     if key_responses:
    #         # Создаем инлайн-кнопки для каждого ключевого слова
    #         keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #             [InlineKeyboardButton(text=key, callback_data=f"show_key_{key}")] for key in key_responses.keys()
    #         ])
    #         await message.answer("❗*ВНИМАНИЕ - ДЕЙСТВИЕ НЕОБРАТИМО*❗", parse_mode="Markdown")
    #         await message.answer("Выберите ключевое слово для удаления:", reply_markup=keyboard)
    #     else:
    #         await message.answer("Список ключевых слов пуст.")

    if message.text == "Список ключевых слов":  # Нажатие на кнопку
        # Если эта кнопка нажата во время процесса добавления key-value
        data = await state.get_data()
        if "keyword" in data:
            await message.answer(f"❗ Процесс добавления `{data.get('keyword')}` был прерван!", parse_mode="Markdown")
            await state.clear()  # Сбрасываем состояние

        # key_responses = await load_key_responses()  # Загружаем список ключевых слов и их значений
        # if key_responses:
        #     response = "Список ключевых слов и их значений:\n\n"
        #     for key, value in key_responses.items():
        #         response += f"❓ `{key}`\n❗ {value}\n➖➖➖➖➖\n"
        #     await message.answer(response, parse_mode="Markdown")
        # else:
        #     await message.answer("Список ключевых слов пуст.")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------


# Функция добавления ключевого слова (для inline и reply)
async def create_key(message: types.Message, state: FSMContext):
    keyword = message.text  # Получаем текст сообщения
    
    # Загружаем текущие ключи из базы данных
    # key_responses = await load_key_responses()
    # Проверяем, существует ли ключевое слово в базе данных
    # if keyword in key_responses:
    #     # Если ключ уже существует, сообщаем об этом пользователю и просим выбрать другое
    #     keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
    #     ])
    #     await message.reply(f"❗❗❗ \n\n➖ {keyword}\n\nУже существует в базе данных.\nПопробуйте другое", reply_markup=keyboard)
    #     await state.clear()  # Сбрасываем состояние
    #     await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key
    # else:
    #     # Если ключа нет, сохраняем его в состоянии и запрашиваем значение
    #     await state.update_data(keyword=keyword)  # Сохраняем ключевое слово в состоянии
    #     keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #         [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
    #     ])
    #     await message.reply(f"Вы ввели ключевое слово:\n➖  {keyword}\n\n➡️  Теперь введите, что будет отвечать бот на это слово", reply_markup=keyboard)
    #     await state.set_state(Form.waiting_for_value)  # Устанавливаем состояние для value

# Обработчик ключевого слова
@dp.message(Form.waiting_for_keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    await create_key(message, state)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Функция добавления значения (для inline и reply)
async def create_value(message: types.Message, state: FSMContext):
    value = message.text  # Получаем текст сообщения
    await state.update_data(value=value)  # Сохраняем значение в состоянии

    # Получаем данные из состояния
    data = await state.get_data()
    keyword = data.get("keyword")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="create_new_word_and_value")],
        [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
    ])
    await message.reply(f"Вы ввели значение:\n➖  {value}\n\nБот будет искать:\n➖ {keyword}\nБот будет отвечать:\n➖  {value}\n\nПодтвердить?", reply_markup=keyboard)

# Обработчик значения
@dp.message(Form.waiting_for_value)
async def process_value(message: types.Message, state: FSMContext):
    await create_value(message, state)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик inline-кнопок
@dp.callback_query()
async def btn_callback(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    # Создание и прерывание нового слова / ГЛАВНОЕ МЕНЮ (после /start)
    if callback_query.data == "add_key_value_btn":  # Кнопка Добавить ключевое слово
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value_null")],
        ])
        await callback_query.message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key

    # / ГЛАВНОЕ МЕНЮ (после /start)
    if callback_query.data == "del_key_value_btn":  # Кнопка Удалить ключевое слово
        await callback_query.message.answer("Вы нажали Кнопку B!")

    # Список всех ключевых слов / ГЛАВНОЕ МЕНЮ (после /start)
    if callback_query.data == "all_key_value_btn":  # Кнопка Список ключевых слов
        # Если эта кнопка нажата во время процесса добавления key-value
        data = await state.get_data()
        if "keyword" in data:
            await callback_query.message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
            await state.clear()  # Сбрасываем состояние

        # key_responses = await load_key_responses()  # Загружаем список ключевых слов и их значений
        # if key_responses:
        #     response = "Список ключевых слов и их значений:\n\n"
        #     for key, value in key_responses.items():
        #         response += f"❓ `{key}`\n❗ {value}\n➖➖➖➖➖\n"
        #     await callback_query.message.answer(response, parse_mode="Markdown")
        # else:
        #     await callback_query.message.answer("Список ключевых слов пуст.")
        # await state.clear()  # Сбрасываем состояние
    #-------------------------------------------------------------------------

    # Конечное создание и прерывание нового слова
    if callback_query.data == "create_new_word_and_value": # Кнопка Подтвердить
        # Получаем данные из состояния
        data = await state.get_data()
        keyword = data.get("keyword")
        value = data.get("value")

        if keyword != None or value != None:
            # Добавляем данные в базу данных
            # await add_db_info(keyword, value)

            # Отправляем сообщение об успешном добавлении
            await callback_query.message.answer(f"✅  Добавлено:\n\n➖  Ключевое слово: {keyword}\n➖  Реакция бота: {value}")
        else:
            await callback_query.message.answer(f"❗ Уже добавлено")

        # Очищаем состояние
        await state.clear()

    # Прервать
    if callback_query.data == "cancel_new_word_and_value":  # Кнопка Прервать (если в памяти уже есть key или value)
        data = await state.get_data()
        if "keyword" in data:
            await callback_query.message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
        await state.clear()

    if callback_query.data == "cancel_new_word_and_value_null":  # Кнопка Прервать (если в памяти ничего нет)
        # Если новым сообщением
        await callback_query.message.answer(f"❗ Процес добавления был прерван!")

        # Если не новым сообщением
        # menu = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        # await callback_query.message.answer("Выберите действие:", reply_markup=menu)
        # await bot.edit_message_text(
        #     chat_id=chat_id,
        #     message_id=message_id,
        #     text="Выберите действие:",
        #     reply_markup=menu,
        # )

        await state.clear()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Запуск бота через start_polling()
async def start():
    await dp.start_polling(bot)  # Передаем бота в start_polling

# Функция для запуска бота
async def edit_key_bot_grp_start_bot():
    await start()