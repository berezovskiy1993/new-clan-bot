import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Загружаем переменные окружения (только через Render)
TOKEN = os.environ.get("API_TOKEN")  # Токен бота
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # ID администратора (для отправки заявок)
GROUP_ID = -1002640250280  # ID группы для дублирования заявок (можно вынести в .env)

# Определение этапов анкеты (используются как состояния в ConversationHandler)
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, MATCHES_CURRENT, SCREENSHOT_1, KD_PREVIOUS, MATCHES_PREVIOUS, SCREENSHOT_2 = range(11)

# Список админов (отображается по кнопке "Админы")
ADMINS = [
    "@DektrianTV - Лидер всех кланов",
    "@Ffllooffy - Зам основы и Лидер Еспортс",
    "@RinaSergeevna - Зам основы",
    "@FRUKTIK58 - Зам основы",
    "@HEADTRICK2 - Зам Еспортс",
    "@neverforgotme - Лидер Академки",
    "@Vasvyu6 - Зам Академки",
    "@kinderskayad - Зам Академки"
]

# Кнопки, отображающиеся во всех этапах анкеты
def get_buttons():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Меню", callback_data='menu'),
        InlineKeyboardButton("Сначала", callback_data='reset_button')
    ]])

# Кнопки меню
def get_menu_buttons():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Критерии", callback_data='criteria_button')
    ], [
        InlineKeyboardButton("Админы", callback_data='admins_button')
    ], [
        InlineKeyboardButton("Соцсети", callback_data='socials_button')
    ], [
        InlineKeyboardButton("⬅ Назад", callback_data='back_button')
    ]])

# Команда /start запускает анкету
async def start(update: Update, context: CallbackContext) -> int:
    # Отправка изображения (логотип/приветствие)
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",
        caption=" "
    )
    # Приветственное сообщение с описанием кланов
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Ты попал в бот клана DEKTRIAN FAMILY!\n"
        "Здесь ты можешь подать заявку в один из кланов:\n\n"
        "▫️ FAMILY — основной клан\n"
        "▫️ ESPORTS — клан для турнирных составов\n"
        "▫️ ACADEMY — клан свободного стиля\n\n"
        "Напиши текстом 'да' и проходи анкету 📝\n\n",
        reply_markup=get_buttons()
    )
    return READY

# Этап подтверждения участия в анкете
async def ready(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    if text == "да":
        await update.message.reply_text("Отлично! Напиши свой игровой никнейм.", reply_markup=get_buttons())
        return NICKNAME
    elif text == "нет":
        await update.message.reply_text("Если передумаешь, напиши 'да'.", reply_markup=get_buttons())
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.", reply_markup=get_buttons())
        return READY

# Обработка всех кнопок
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        await query.message.edit_reply_markup(reply_markup=get_menu_buttons())
    elif query.data == 'criteria_button':
        await query.message.edit_text(
            "Критерии клана DEKTRIAN FAMILY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд на 100 матчей (Девушки - 4; Мужчины - 5)\n"
            "3. Возраст 16+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "_________________________________\n"
            "Критерии клана DEKTRIAN ACADEMY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд и матчи не важны.\n"
            "3. Возраст 14+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "_________________________________\n"
            "Критерии клана DEKTRIAN ESPORTS:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Возраст 16+\n"
            "3. Наличие результатов и хайлайтов\n"
            "4. Преимущество отдается собранным пакам\n",
            reply_markup=get_menu_buttons()
        )
    elif query.data == 'admins_button':
        await query.message.edit_text("Список админов:\n" + "\n".join(ADMINS), reply_markup=get_menu_buttons())
    elif query.data == 'socials_button':
        socials_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("YouTube", url="https://www.youtube.com/@Dektrian_TV")],
            [InlineKeyboardButton("Twitch", url="https://www.twitch.tv/dektrian_tv")],
            [InlineKeyboardButton("Группа Telegram", url="https://t.me/dektrian_tv")],
            [InlineKeyboardButton("Канал Telegram", url="https://t.me/dektrian_family")],
            [InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@dektrian_tv")],
            [InlineKeyboardButton("⬅ Назад", callback_data='back_button')]
        ])
        await query.message.edit_text("Выберите платформу:", reply_markup=socials_keyboard)
    elif query.data == 'back_button':
        # Возвращаем пользователя в главное меню
        await query.message.edit_reply_markup(reply_markup=get_menu_buttons())
        await query.message.edit_text("Вы в главном меню. Выберите нужную опцию:", reply_markup=get_menu_buttons())

# Основная функция запуска бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Обработка анкеты по этапам
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            READY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ready), CallbackQueryHandler(button_callback)],
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nickname), CallbackQueryHandler(button_callback)],
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_id), CallbackQueryHandler(button_callback)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age), CallbackQueryHandler(button_callback)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender), CallbackQueryHandler(button_callback)],
            KD_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_current), CallbackQueryHandler(button_callback)],
            MATCHES_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_current), CallbackQueryHandler(button_callback)],
            SCREENSHOT_1: [MessageHandler(filters.PHOTO, screenshot_1), CallbackQueryHandler(button_callback)],
            KD_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_previous), CallbackQueryHandler(button_callback)],
            MATCHES_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_previous), CallbackQueryHandler(button_callback)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO, screenshot_2), CallbackQueryHandler(button_callback)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запуск бота через webhook (используется на Render)
    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == "__main__":
    main()
