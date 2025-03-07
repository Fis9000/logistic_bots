from telegram import Bot
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tg_bots.feedback_bot_grp.json_handler import add_db_info, load_key_responses  # Изменено на импорт из json_handler
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
async def cmd_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "keyword" in data:
        await message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
        await state.clear()  # Сбрасываем состояние

    menu = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await send_reply_buttons(message.chat.id, "Здесь Вы можете добавить или удалить ключевые слова для бота обатной связи")  # Отправляем reply-кнопки при /start
    await message.answer("Выберите действие:", reply_markup=menu)

# Обработчик reply-кнопок
@dp.message(lambda message: message.text in ["Добавить ключевое слово", "Удалить ключевое слово", "Список ключевых слов"])
async def process_reply_buttons(message: types.Message, state: FSMContext):
    if message.text == "Добавить ключевое слово":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value_null")],
        ])
        await message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)

    if message.text == "Удалить ключевое слово":
        key_responses = await load_key_responses()
        if key_responses:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=key, callback_data=f"show_key_{key}")] for key in key_responses.keys()
            ])
            await message.answer("❗*ВНИМАНИЕ - ДЕЙСТВИЕ НЕОБРАТИМО*❗", parse_mode="Markdown")
            await message.answer("Выберите ключевое слово для удаления:", reply_markup=keyboard)
        else:
            await message.answer("Список ключевых слов пуст.")

    if message.text == "Список ключевых слов":
        data = await state.get_data()
        if "keyword" in data:
            await message.answer(f"❗ Процесс добавления `{data.get('keyword')}` был прерван!", parse_mode="Markdown")
            await state.clear()

        key_responses = await load_key_responses()
        if key_responses:
            response = "Список ключевых слов и их значений:\n\n"
            for key, value in key_responses.items():
                response += f"❓ `{key}`\n❗ {value}\n➖➖➖➖➖\n"
            await message.answer(response, parse_mode="Markdown")
        else:
            await message.answer("Список ключевых слов пуст.")

# Функция добавления ключевого слова
async def create_key(message: types.Message, state: FSMContext):
    keyword = message.text
    key_responses = await load_key_responses()
    if keyword in key_responses:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await message.reply(f"❗❗❗ \n\n➖ {keyword}\n\nУже существует в базе данных.\nПопробуйте другое", reply_markup=keyboard)
        await state.clear()
        await state.set_state(Form.waiting_for_keyword)
    else:
        await state.update_data(keyword=keyword)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
        ])
        await message.reply(f"Вы ввели ключевое слово:\n➖  {keyword}\n\n➡️  Теперь введите, что будет отвечать бот на это слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_value)

@dp.message(Form.waiting_for_keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    await create_key(message, state)

# Функция добавления значения
async def create_value(message: types.Message, state: FSMContext):
    value = message.text
    await state.update_data(value=value)
    data = await state.get_data()
    keyword = data.get("keyword")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="create_new_word_and_value")],
        [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value")],
    ])
    await message.reply(f"Вы ввели значение:\n➖  {value}\n\nБот будет искать:\n➖ {keyword}\nБот будет отвечать:\n➖  {value}\n\nПодтвердить?", reply_markup=keyboard)

@dp.message(Form.waiting_for_value)
async def process_value(message: types.Message, state: FSMContext):
    await create_value(message, state)

# Обработчик inline-кнопок
@dp.callback_query()
async def btn_callback(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    if callback_query.data == "add_key_value_btn":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word_and_value_null")],
        ])
        await callback_query.message.answer("➡️  Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)

    if callback_query.data == "del_key_value_btn":
        await callback_query.message.answer("Вы нажали Кнопку B!")

    if callback_query.data == "all_key_value_btn":
        data = await state.get_data()
        if "keyword" in data:
            await callback_query.message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
            await state.clear()

        key_responses = await load_key_responses()
        if key_responses:
            response = "Список ключевых слов и их значений:\n\n"
            for key, value in key_responses.items():
                response += f"❓ `{key}`\n❗ {value}\n➖➖➖➖➖\n"
            await callback_query.message.answer(response, parse_mode="Markdown")
        else:
            await callback_query.message.answer("Список ключевых слов пуст.")
        await state.clear()

    if callback_query.data == "create_new_word_and_value":
        data = await state.get_data()
        keyword = data.get("keyword")
        value = data.get("value")

        if keyword != None or value != None:
            await add_db_info(keyword, value)
            await callback_query.message.answer(f"✅  Добавлено:\n\n➖  Ключевое слово: {keyword}\n➖  Реакция бота: {value}")
        else:
            await callback_query.message.answer(f"❗ Уже добавлено")

        await state.clear()

    if callback_query.data == "cancel_new_word_and_value":
        data = await state.get_data()
        if "keyword" in data:
            await callback_query.message.answer(f"❗ Процес добавления `{data.get("keyword")}` был прерван!", parse_mode="Markdown")
        await state.clear()

    if callback_query.data == "cancel_new_word_and_value_null":
        await callback_query.message.answer(f"❗ Процес добавления был прерван!")
        await state.clear()

# Запуск бота через start_polling()
async def start():
    await dp.start_polling(bot)

# Функция для запуска бота
async def edit_key_bot_grp_start_bot():
    await start()