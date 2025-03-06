from email import message
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from tg_bots.feedback_bot_grp.db import add_db_info, load_key_responses
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

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("Добавить ключевое слово"), callback_data = "add_key_value_btn")],
        [InlineKeyboardButton(text=("Удалить ключевое слово"), callback_data = "del_key_value_btn")],
        [InlineKeyboardButton(text=("Список ключевых слов"), callback_data = "all_key_value_btn")],
    ])
    await send_reply_buttons(message.chat.id, "Здесь Вы можете добавить или удалить ключевые слова для бота обатной связи")  # Отправляем reply-кнопки при /start
    await message.answer("Выберите действие:", reply_markup=menu)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик reply-кнопок
@dp.message(lambda message: message.text in ["Добавить ключевое слово", "Удалить ключевое слово", "Список ключевых слов", "test"])
async def process_reply_buttons(message: types.Message, state: FSMContext):
    if message.text == "Добавить ключевое слово":  # Нажатие на кнопку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key

    if message.text == "Удалить ключевое слово":  # Нажатие на кнопку
        await message.answer("Вы нажали Кнопку B!")

    if message.text == "test":
        add_db_info("t1", "test")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------


# Функция добавления ключевого слова (для inline и reply)
async def create_key(message: types.Message, state: FSMContext):
    keyword = message.text  # Получаем текст сообщения
    
    # Загружаем текущие ключи из базы данных
    key_responses = await load_key_responses()
    # Проверяем, существует ли ключевое слово в базе данных
    if keyword in key_responses:
        # Если ключ уже существует, сообщаем об этом пользователю и просим выбрать другое
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await message.reply(f"Ключевое слово\n\n➖ {keyword}\n\nУже существует в базе данных.\nПопробуйте другое", reply_markup=keyboard)
        await state.clear()  # Сбрасываем состояние
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key
    else:
        # Если ключа нет, сохраняем его в состоянии и запрашиваем значение
        await state.update_data(keyword=keyword)  # Сохраняем ключевое слово в состоянии
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await message.reply(f"Вы ввели ключевое слово:\n\n➖  {keyword}\n\n➡️  Теперь введите, что будет отвечать бот на это слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_value)  # Устанавливаем состояние для value

# Обработчик ключевого слова
@dp.message(Form.waiting_for_keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    await create_key(message, state)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Функция добавления значения (для inline и reply)
async def create_value(message: types.Message, state: FSMContext):
    value = message.text  # Получаем текст сообщения
    await state.update_data(value=value)  # Сохраняем значение в состоянии
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="create_new_word_and_value")],
        [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
    ])
    await message.reply(f"Вы ввели значение:\n\n➖  {value}\n\nПодтвердить?", reply_markup=keyboard)

# Обработчик значения
@dp.message(Form.waiting_for_value)
async def process_value(message: types.Message, state: FSMContext):
    await create_value(message, state)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик inline-кнопок
@dp.callback_query()
async def btn_callback(callback_query: types.CallbackQuery, state: FSMContext):
    # ГЛАВНОЕ МЕНЮ (после /start)
    # Создание и прерывание нового слова
    if callback_query.data == "add_key_value_btn":  # Кнопка Добавить ключевое слово
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await callback_query.message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние для key

    if callback_query.data == "del_key_value_btn":  # Кнопка Удалить ключевое слово
        await callback_query.message.answer("Вы нажали Кнопку B!")
        
    # Конечное создание и прерывание нового слова
    if callback_query.data == "create_new_word_and_value": # Кнопка Подтвердить
        # Получаем данные из состояния
        data = await state.get_data()
        keyword = data.get("keyword")
        value = data.get("value")

        if keyword != None or value != None:
            # Добавляем данные в базу данных
            await add_db_info(keyword, value)

            # Отправляем сообщение об успешном добавлении
            await callback_query.message.answer(f"✅  Добавлено:\n\n➖  Ключевое слово: {keyword}\n➖  Реакция бота: {value}")
        else:
            await callback_query.message.answer(f"❗ Уже добавлено")

        # Очищаем состояние
        await state.clear()
    if callback_query.data == "cancel_new_word_and_value":  # Кнопка Прервать
        await callback_query.message.answer("❗Отмена")
        await state.clear()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Запуск бота через start_polling()
async def start():
    await dp.start_polling(bot)  # Передаем бота в start_polling

# Функция для запуска бота
async def edit_key_bot_grp_start_bot():
    await start()