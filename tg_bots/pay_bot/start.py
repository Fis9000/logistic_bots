import emoji
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from globals import GlobalConfig

# Токен бота
TELEGRAM_TOKEN = GlobalConfig.pay_tg_bot_token

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрируем бота в диспетчере
dp["bot"] = bot

# Обработчик команды /start
@dp.message()
async def start_command(message: types.Message):
    if message.text == "/start":
        await message.answer(
            "Приветствуем в Атлант Санкт-Петербург!\n\n"
            "Для получения возможности писать в [👷‍♂️АТЛАНТ СПБ👷‍♂️ ХАЛТУРА СПБ | ПОДРАБОТКА СПБ | ШАБАШКА СПБ | РАБОТА САНКТ-ПЕТЕРБУРГ | РАБОТА ПИТЕР](https://t.me/+ohMa5RfNTOkyZDcy?disable_preview=true), "
            "оплатите тариф с нужным количеством сообщений.",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        # Кнопки тарифов
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="15 публикаций", callback_data="tariff_15")],
            [InlineKeyboardButton(text="50 публикаций", callback_data="tariff_50")],
            [InlineKeyboardButton(text="100 публикаций", callback_data="tariff_100")]
        ])
        await message.answer("Доступные тарифы:", reply_markup=keyboard)

# Обработчик кнопок тарифов
@dp.callback_query()
async def tariff_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    # Тариф 15
    if callback_query.data == "tariff_15":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[  # Создаем клавиатуру
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_15")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 15 публикаций\nСтоимость: <s>300.00</s> 250.00 🇷🇺RUB\nКол-во доступных сообщений: 15 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    # Тариф 50
    if callback_query.data == "tariff_50":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_50")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 50 публикаций\nСтоимость: <s>900.00</s> 590.00 🇷🇺RUB\nКол-во доступных сообщений: 50 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    # Тариф 100
    if callback_query.data == "tariff_100":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_100")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 100 публикаций\nСтоимость: <s>1700.00</s> 1050.00 🇷🇺RUB\nКол-во доступных сообщений: 100 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    # Кнопка "Назад"
    if callback_query.data == "back":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="15 публикаций", callback_data="tariff_15")],
            [InlineKeyboardButton(text="50 публикаций", callback_data="tariff_50")],
            [InlineKeyboardButton(text="100 публикаций", callback_data="tariff_100")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Доступные тарифы:",  # Сюда возвращаем текст "Доступные тарифы:"
            reply_markup=keyboard
        )

    # Обработчик для оплаты тарифов
    if callback_query.data == "pay_15":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💰 Юкасса"), callback_data="ukassa_15")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)

    if callback_query.data == "pay_50":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💰 Юкасса"), callback_data="ukassa_50")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)

    if callback_query.data == "pay_100":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💰 Юкасса"), callback_data="ukassa_100")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        
    # Переход к оплате 15
    if callback_query.data == "ukassa_15":
        user_id = callback_query.from_user.id  # Получаем реальный ID пользователя
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("⌛ Я ОПЛАТИЛ"), callback_data="i_paid_15")],
            [InlineKeyboardButton(text=emoji.emojize("🚫 ОТМЕНА"), callback_data="cancel_15")]
        ])
        # Обновляем сообщение с реквизитами для оплаты
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Способ оплаты: Сбербанк\nК оплате: 250.00 🇷🇺RUB\nВаш ID: `{user_id}`\nРеквизиты для оплаты:\n\n2202 2063 1864 9626\n__________________________\n_Вы платите физическому лицу._\n_Деньги поступят на счёт получателя._",
            reply_markup=keyboard,
            parse_mode="Markdown"  # Используем Markdown для форматирования
        )

        # Всплывающее сообщение (alert) для пользователя
        await bot.answer_callback_query(
            callback_query.id,  # Используем ID callback запроса для отправки ответа
            text="✅ После оплаты нажмите кнопку 'Я ОПЛАТИЛ' и следуйте указаниям.",  # Текст уведомления
            show_alert=True  # Показывает уведомление как алерт
        )
    if callback_query.data == "cancel_15":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_15")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        # Обновляем текст и клавиатуру без отправки нового сообщения
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 15 публикаций\nСтоимость: <s>300.00</s> 250.00 🇷🇺RUB\nКол-во доступных сообщений: 15 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    # Переход к оплате 50
    if callback_query.data == "ukassa_50":
        user_id = callback_query.from_user.id  # Получаем реальный ID пользователя
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("⌛ Я ОПЛАТИЛ"), callback_data="i_paid_50")],
            [InlineKeyboardButton(text=emoji.emojize("🚫 ОТМЕНА"), callback_data="cancel_50")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Способ оплаты: Сбербанк\nК оплате: 590.00 🇷🇺RUB\nВаш ID: `{user_id}`\nРеквизиты для оплаты:\n\n2202 2063 1864 9626\n__________________________\n_Вы платите физическому лицу._\n_Деньги поступят на счёт получателя._",
            reply_markup=keyboard,
            parse_mode="Markdown"  # Указываем, что используем Markdown для форматирования
        )
        # Всплывающее сообщение (alert) для пользователя
        await bot.answer_callback_query(
            callback_query.id,  # Используем ID callback запроса для отправки ответа
            text="✅ После оплаты нажмите кнопку 'Я ОПЛАТИЛ' и следуйте указаниям.",  # Текст уведомления
            show_alert=True  # Показывает уведомление как алерт
        )
    if callback_query.data == "cancel_50":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_50")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        # Обновляем текст и клавиатуру без отправки нового сообщения
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 50 публикаций\nСтоимость: <s>900.00</s> 590.00 🇷🇺RUB\nКол-во доступных сообщений: 50 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    # Переход к оплате 100
    if callback_query.data == "ukassa_100":
        user_id = callback_query.from_user.id  # Получаем реальный ID пользователя
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("⌛ Я ОПЛАТИЛ"), callback_data="i_paid_100")],
            [InlineKeyboardButton(text=emoji.emojize("🚫 ОТМЕНА"), callback_data="cancel_100")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Способ оплаты: Сбербанк\nК оплате: 1050.00 🇷🇺RUB\nВаш ID: `{user_id}`\nРеквизиты для оплаты:\n\n2202 2063 1864 9626\n__________________________\n_Вы платите физическому лицу._\n_Деньги поступят на счёт получателя._",
            reply_markup=keyboard,
            parse_mode="Markdown"  # Указываем, что используем Markdown для форматирования
        )
        # Всплывающее сообщение (alert) для пользователя
        await bot.answer_callback_query(
            callback_query.id,  # Используем ID callback запроса для отправки ответа
            text="✅ После оплаты нажмите кнопку 'Я ОПЛАТИЛ' и следуйте указаниям.",  # Текст уведомления
            show_alert=True  # Показывает уведомление как алерт
        )
    if callback_query.data == "cancel_100":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data="pay_100")],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        # Обновляем текст и клавиатуру без отправки нового сообщения
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: 100 публикаций\nСтоимость: <s>1700.00</s> 1050.00 🇷🇺RUB\nКол-во доступных сообщений: 100 шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )


# Запуск бота через start_polling()
async def incoming_messages():
    await dp.start_polling(bot)

# Функция для запуска бота
async def pay_bot_start_bot():
    await incoming_messages()
