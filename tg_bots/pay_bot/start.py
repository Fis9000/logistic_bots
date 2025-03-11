import emoji
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from globals import GlobalConfig

# Токен бота
TELEGRAM_TOKEN = GlobalConfig.pay_tg_bot_token

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрируем бота в диспетчере
dp["bot"] = bot

# Reply-клавиатура
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=emoji.emojize("💳 Оплатить")),
            KeyboardButton(text=emoji.emojize("⏳ Баланс"))
        ]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message()
async def start_command(message: types.Message):
    async def tariff_menu():
        # # Кнопки тарифов
        tariff_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="15 публикаций", callback_data="tariff_15")],
            [InlineKeyboardButton(text="50 публикаций", callback_data="tariff_50")],
            [InlineKeyboardButton(text="100 публикаций", callback_data="tariff_100")]
        ])
        await message.answer("Доступные тарифы:", reply_markup=tariff_keyboard)

    if message.text == "/start":
        await message.answer(
            "Приветствуем в Атлант Санкт-Петербург!\n\n"
            "Для получения возможности писать в [👷‍♂️АТЛАНТ СПБ👷‍♂️ ХАЛТУРА СПБ | ПОДРАБОТКА СПБ | ШАБАШКА СПБ | РАБОТА САНКТ-ПЕТЕРБУРГ | РАБОТА ПИТЕР](https://t.me/+ohMa5RfNTOkyZDcy?disable_preview=true), "
            "оплатите тариф с нужным количеством сообщений.",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_keyboard
        )
        await tariff_menu()

    if message.text == "💳 Оплатить":
        await tariff_menu()

    if message.text == "⏳ Баланс":
        tariff_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оплатить тариф", callback_data="oplatit_tarif")],
        ])
        await message.answer(
            "😬 Вы не можете отправлять сообщения в группе "
            "[👷‍♂️АТЛАНТ СПБ👷‍♂️ ХАЛТУРА СПБ | ПОДРАБОТКА СПБ | ШАБАШКА СПБ | "
            "РАБОТА САНКТ-ПЕТЕРБУРГ | РАБОТА ПИТЕР](https://t.me/+ohMa5RfNTOkyZDcy?disable_preview=true), "
            "т.к. у вас нет оплаченного тарифа.\n\n"
            "**⬇️ Оплатите подходящий тариф.**",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=tariff_keyboard
        )

@dp.callback_query()
async def tariff_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    ### Меню выбора тарифа
    async def tarif_menu(_pay_btn, _tarif_count, _summ_old, _summ_new):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💳 Оплатить"), callback_data=_pay_btn)],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тариф: " + _tarif_count + " публикаций\nСтоимость: <s>" + _summ_old + "</s> " + _summ_new + " 🇷🇺RUB\nКол-во доступных сообщений: " + _tarif_count + " шт",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    # Тариф 15
    if callback_query.data == "tariff_15":
        await tarif_menu("pay_15", "15","300.00", "250.00")
    # Тариф 50
    if callback_query.data == "tariff_50":
        await tarif_menu("pay_50", "50","900.00", "590.00")
    # Тариф 100
    if callback_query.data == "tariff_100":
        await tarif_menu("pay_100", "100", "1700.00", "1050.00")
    ###
    
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
            text="Доступные тарифы:",
            reply_markup=keyboard
        )

    ### Меню оплаты тарифов до нажатия оплатить
    async def pay_menu_before(_ukassa_btn):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("💰 Юкасса"), callback_data=_ukassa_btn)],
            [InlineKeyboardButton(text=emoji.emojize("⬅️ Назад"), callback_data="back")]
        ])
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
    # Оплатить 15
    if callback_query.data == "pay_15":
        await pay_menu_before("ukassa_15")
    # Оплатить 50
    if callback_query.data == "pay_50":
        await pay_menu_before("ukassa_50")
    # Оплатить 100
    if callback_query.data == "pay_100":
        await pay_menu_before("ukassa_100")
    ###

    ### Меню оплаты тарифов после нажатия оплатить   
    async def pay_menu_after(_i_paid_btn, _cancel_btn, _summ):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("⌛ Я ОПЛАТИЛ"), callback_data=_i_paid_btn)],
            [InlineKeyboardButton(text=emoji.emojize("🚫 ОТМЕНА"), callback_data=_cancel_btn)]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Способ оплаты: Сбербанк\nК оплате: " + _summ + " 🇷🇺RUB\nВаш ID: `" + str(user_id) + "`\nРеквизиты для оплаты:\n\n2202 2063 1864 9626\n__________________________\n_Вы платите физическому лицу._\n_Деньги поступят на счёт получателя._",
            reply_markup=keyboard,
            parse_mode="Markdown"  # Используем Markdown для форматирования
        )
        # Всплывающее сообщение (alert)
        await bot.answer_callback_query(
            callback_query.id,
            text="✅ После оплаты нажмите кнопку 'Я ОПЛАТИЛ' и следуйте указаниям.",
            show_alert=True
        )
    # Переход к оплате 15
    if callback_query.data == "ukassa_15":
        await pay_menu_after("i_paid_15", "cancel_15", "250.00")
    # Отмена оплаты 15    
    if callback_query.data == "cancel_15":
        await tarif_menu("pay_15", "15","300.00", "250.00") # Возвращаемся в меню выбота тарифа

    # Переход к оплате 50
    if callback_query.data == "ukassa_50":
        await pay_menu_after("i_paid_50", "cancel_50", "590.00")
    # Отмена оплаты 50    
    if callback_query.data == "cancel_50":
        await tarif_menu("pay_50", "50","900.00", "590.00") # Возвращаемся в меню выбота тарифа

    # Переход к оплате 100
    if callback_query.data == "ukassa_100":
        await pay_menu_after("i_paid_100", "cancel_100", "1050.00")
    # Отмена оплаты 100    
    if callback_query.data == "cancel_100":
        await tarif_menu("pay_100", "100", "1700.00", "1050.00") # Возвращаемся в меню выбота тарифа
    ###

    ### Кнопки "Я ОПЛАТИЛ"
    async def i_paid(_cancel_btn):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=emoji.emojize("🚫 ОТМЕНА"), callback_data=_cancel_btn)]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"💁🏻‍♂️ Оплатили?\n\n👌🏻 Тогда отправьте сюда картинкой (не документом!) квитанцию платежа: скриншот или фото.\n\nНа квитанции должны быть четко видны: дата, время и сумма платежа.\n__________________________\nЗа спам вы можете быть заблокированы!",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    if callback_query.data == "i_paid_15":
        await i_paid("cancel_15")
    if callback_query.data == "i_paid_50":
        await i_paid("cancel_50")
    if callback_query.data == "i_paid_100":
        await i_paid("cancel_100")
    ###

    ### Кнопка "Оплатить тариф"
    if callback_query.data == "oplatit_tarif":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="15 публикаций", callback_data="tariff_15")],
            [InlineKeyboardButton(text="50 публикаций", callback_data="tariff_50")],
            [InlineKeyboardButton(text="100 публикаций", callback_data="tariff_100")]
        ])
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Доступные тарифы:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
# Запуск бота через start_polling()
async def incoming_messages():
    await dp.start_polling(bot)

# Функция для запуска бота
async def pay_bot_start_bot():
    await incoming_messages()