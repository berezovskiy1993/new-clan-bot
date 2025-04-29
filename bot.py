from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора и группы
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843
GROUP_ID = -1002640250280

# Определение этапов диалога
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, MATCHES_CURRENT, SCREENSHOT_1, KD_PREVIOUS, MATCHES_PREVIOUS, SCREENSHOT_2 = range(11)

# Список админов
ADMINS = ["@Admin1", "@Admin2", "@Admin3"]

# Кнопки внизу каждого шага
def get_buttons():
    keyboard = [
        [
            InlineKeyboardButton("Меню", callback_data='menu'),
            InlineKeyboardButton("Отмена", callback_data='reset_button')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Кнопки меню
def get_menu_buttons():
    keyboard = [
        [InlineKeyboardButton("Критерии", callback_data='criteria_button')],
        [InlineKeyboardButton("Админы", callback_data='admins_button')],
        [InlineKeyboardButton("Соцсети", callback_data='socials_button')],
        [InlineKeyboardButton("⬅ Назад", callback_data='back_button')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Начало общения с ботом
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",
        caption=" "
    )
    await update.message.reply_text(
        "Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан — напишите 'да' или 'нет'.",
        reply_markup=get_buttons()
    )
    return READY

# Ответ на "да"/"нет" — переход к никнейму
async def ready(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text.lower()
    if user_response == 'да':
        await update.message.reply_text("Отлично! Напиши свой игровой никнейм.")
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("Если передумаешь, напиши 'да'.")
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.")
        return READY

# Запись никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text("Теперь укажи свой игровой айди.", reply_markup=get_buttons())
    return PLAYER_ID

# Запись ID
async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text("Сколько тебе полных лет?", reply_markup=get_buttons())
    return AGE

# Запись возраста
async def age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text("Ты девочка или парень?", reply_markup=get_buttons())
    return GENDER

# Запись пола
async def gender(update: Update, context: CallbackContext) -> int:
    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text("Какая у тебя КД за текущий сезон?", reply_markup=get_buttons())
    return KD_CURRENT

# Запись КД текущего сезона
async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в текущем сезоне?", reply_markup=get_buttons())
    return MATCHES_CURRENT

# Запись матчей текущего сезона
async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text("Отправь скриншот статистики за текущий сезон.", reply_markup=get_buttons())
    return SCREENSHOT_1

# Получение скриншота текущего сезона
async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id
        await update.message.reply_text("Теперь укажи КД за прошлый сезон.", reply_markup=get_buttons())
        return KD_PREVIOUS
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.")
        return SCREENSHOT_1

# Запись КД прошлого сезона
async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в прошлом сезоне?", reply_markup=get_buttons())
    return MATCHES_PREVIOUS

# Запись матчей прошлого сезона
async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text("Теперь отправь скриншот за прошлый сезон.", reply_markup=get_buttons())
    return SCREENSHOT_2

# Получение скриншота прошлого сезона и отправка заявки
async def screenshot_2(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id
        telegram_username = update.message.from_user.username
        telegram_user_id = update.message.from_user.id

        # Формирование заявки
        application = (
            f"Заявка на вступление в клан DEKTRIAN FAMILY:\n"
            f"Игровой ник: {context.user_data['nickname']}\n"
            f"Игровой айди: {context.user_data['player_id']}\n"
            f"Возраст: {context.user_data['age']}\n"
            f"Пол: {context.user_data['gender']}\n"
            f"КД за текущий сезон: {context.user_data['kd_current']}\n"
            f"Матчи в текущем сезоне: {context.user_data['matches_current']}\n"
            f"КД за прошлый сезон: {context.user_data['kd_previous']}\n"
            f"Матчи в прошлом сезоне: {context.user_data['matches_previous']}\n"
            f"Telegram Username: @{telegram_username}\n"
            f"Telegram UserID: {telegram_user_id}\n"
        )

        # Отправка заявки админам и в группу
        try:
            await context.bot.send_message(ADMIN_ID, application)
            await context.bot.send_message(GROUP_ID, application)
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_2'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_2'])
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке: {e}")

        await update.message.reply_text(
            "Ваша заявка отправлена, ожидайте ответ в течение дня! Если появились вопросы — напишите Лидеру @DektrianTV.",
            reply_markup=get_buttons()
        )
    return ConversationHandler.END

# Сброс анкеты
async def reset(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.edit_text(
        "Все данные были сброшены. Начни процесс заново, введя свой игровой никнейм.",
        reply_markup=get_buttons()
    )
    return NICKNAME

# Обработка всех кнопок
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'reset_button':
        return await reset(update, context)
    elif query.data == 'menu':
        await query.message.edit_reply_markup(reply_markup=get_menu_buttons())
    elif query.data == 'back_button':
        await query.message.edit_reply_markup(reply_markup=get_buttons())
    elif query.data == 'criteria_button':
        await query.message.edit_text(
            "Критерии клана DEKTRIAN FAMILY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд на 100 матчей (Девушки — 4; Мужчины — 5)\n"
            "3. Возраст 16+\n"
            "4. Актив в чате\n"
            "5. Участие в стримах и мероприятиях\n\n"
            "ACADEMY: без ограничений по КД и матчам, 14+\n"
            "ESPORTS: 16+, результаты, хайлайты, паки.",
            reply_markup=get_menu_buttons()
        )
    elif query.data == 'admins_button':
        await query.message.edit_text("Список админов:\n" + "\n".join(ADMINS), reply_markup=get_menu_buttons())
    elif query.data == 'socials_button':
        await query.message.edit_text(
            "Соцсети Лидера клана:\n\n"
            "YouTube: https://youtube.com/@Dektrian\n"
            "Twitch: https://twitch.tv/dektrian\n"
            "Группа Telegram: https://t.me/dektrian_family\n"
            "Канал Telegram: https://t.me/dektrian_channel\n"
            "TikTok: https://tiktok.com/@dektriantv",
            reply_markup=get_menu_buttons()
        )

# Основная функция запуска бота
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
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

    application.add_handler(conversation_handler)
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запуск вебхука
    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == '__main__':
    main()
