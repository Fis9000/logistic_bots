from email import message
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from globals import GlobalConfig

# Токен бота
TELEGRAM_TOKEN = GlobalConfig.edit_feedback_tg_bot_token
GROUP_ID = GlobalConfig.edit_feedback_tg_bot_group_id

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Класс для хранения состояний
class Form(StatesGroup):
    waiting_for_keyword = State()  # Состояние ожидания ключевого слова

# Функция для отправки reply-кнопок в группу
async def send_reply_buttons(chat_id, _text):
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ключевое слово"), KeyboardButton(text="Удалить ключевое слово")]
        ],
        resize_keyboard=True 
    )
    await bot.send_message(chat_id, _text, reply_markup=reply_keyboard)

@dp.message(lambda message: message.new_chat_members)
async def on_new_member(message: types.Message):
    for user in message.new_chat_members:        
        user_name = user.first_name # Получаем имя пользователя
        if user.last_name:
            user_name += f" {user.last_name}"
    await send_reply_buttons(message.chat.id, "Новый пользователь: " + user_name + "") # Отправляем reply-кнопки каждому новому пользователю 
    # await send_reply_buttons(GROUP_ID, "Новый пользователь: " + user_name + "") # Отправляем reply-кнопки каждому новому пользователю 

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await send_reply_buttons(message.chat.id, "Выберите действие:") # Отправляем reply-кнопки при /start    
    # await send_reply_buttons(GROUP_ID, "Выберите действие:") # Отправляем reply-кнопки при /start    

# Обработчик reply-кнопок
@dp.message(lambda message: message.text in ["Добавить ключевое слово", "Удалить ключевое слово"])
async def process_reply_buttons(message: types.Message, state: FSMContext):
    if message.text == "Добавить ключевое слово": # Нажатие на кнопку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word")],
        ])
        await message.reply("Напишите ключевое слово", reply_markup=keyboard)
        await state.set_state(Form.waiting_for_keyword)  # Устанавливаем состояние
    elif message.text == "Удалить ключевое слово": # Нажатие на кнопку
        await message.reply("Вы нажали Кнопку B!")

# Обработчик состояния ожидания ключевого слова
@dp.message(Form.waiting_for_keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    keyword = message.text  # Получаем текст сообщения
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прервать", callback_data="cancel_new_word")],
    ])
    await message.reply(f"Вы ввели ключевое слово: {keyword}\n\nТеперь введите что будет отвечать бот на это слово", reply_markup=keyboard)
    await state.clear()  # Сбрасываем состояние
    
# Запуск бота через start_polling()
async def start():
    await dp.start_polling(bot)  # Передаем бота в start_polling

# Функция для запуска бота
async def edit_key_bot_grp_start_bot():
    await start()