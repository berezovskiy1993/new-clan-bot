from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2 = range(11)

# Список админов клана
ADMINS = ["@Admin1", "@Admin2", "@Admin3"]  # Замените на реальные никнеймы админов

# Функция для создания кнопок
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data='reset_button')],
        [InlineKeyboardButton("Критерии", callback_data='criteria_button')],
        [InlineKeyboardButton("Админы", callback_data='admins_button')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",
        caption=" "
    )
    await update.message.reply_text(
        "Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан - напишите 'да' или 'нет'.",
        reply_markup=get_buttons()
    )
    return READY

# Проверка на готовность подать заявку
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

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь, пожалуйста, укажи свой игровой айди.",
        reply_markup=get_buttons()
    )
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text(
        "Сколько тебе полных лет?",
        reply_markup=get_buttons()
    )
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    # Проверяем, нажата ли кнопка "Отмена"
    if update.message.text.lower() == 'отмена':
        context.user_data.clear()
        await update.message.reply_text(
            "Отмена процесса. Давайте начнем сначала. Напишите свой игровой никнейм:",
            reply_markup=get_buttons()
        )
        return NICKNAME

    # Иначе продолжаем обычную логику
    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        "Ты девочка или парень?",
        reply_markup=get_buttons()
    )
    return GENDER

# Получение пола
async def gender(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'отмена':
        context.user_data.clear()
        await update.message.reply_text(
            "Отмена процесса. Давайте начнем сначала. Напишите свой игровой никнейм:",
            reply_markup=get_buttons()
        )
        return NICKNAME

    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text(
        "Какая у тебя КД за текущий сезон?",
        reply_markup=get_buttons()
    )
    return KD_CURRENT

# Получение КД за текущий сезон
async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text(
        "Какой у тебя КД за прошлый сезон?",
        reply_markup=get_buttons()
    )
    return KD_PREVIOUS

# Получение КД за прошлый сезон
async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в текущем сезоне?",
        reply_markup=get_buttons()
    )
    return MATCHES_CURRENT

# Получение матчей за текущий сезон
async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в прошлом сезоне?",
        reply_markup=get_buttons()
    )
    return MATCHES_PREVIOUS

# Получение матчей за прошлый сезон
async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text(
        "Пожалуйста, отправь скриншот статистики из игры за текущий сезон.",
        reply_markup=get_buttons()
    )
    return SCREENSHOT_1

# Получение первого скриншота
async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id
        await update.message.reply_text(
            "Теперь отправь скриншот статистики за прошлый сезон.",
            reply_markup=get_buttons()
        )
        return SCREENSHOT_2
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.")
        return SCREENSHOT_1

# Получение второго скриншота
async def screenshot_2(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id
        
        telegram_username = update.message.from_user.username
        telegram_user_id = update.message.from_user.id        
        
        application_text = (
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

        try:
            await context.bot.send_message(ADMIN_ID, application_text)
            await context.bot.send_message(GROUP_ID, application_text)
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_2'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_2'])
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке: {e}")

        await update.message.reply_text(
            "Ваша заявка отправлена, ожидайте ответ в течение дня! Если возникли вопросы, напишите Лидеру клана @DektrianTV.",
            reply_markup=get_buttons()
        )
        
    return ConversationHandler.END

# ВАЖНО: Новый сброс
async def reset(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data.clear()  # Полный сброс данных

    await query.message.edit_text(
        "🔄 Все данные были сброшены.\n\nНапишите 'да' или 'нет', чтобы начать подачу заявки заново!",
        reply_markup=get_buttons()
    )
    return READY  # <-- ВАЖНО: возвращаем на начало "Готов?"

# Обработка кнопок
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'reset_button':
        return await reset(update, context)
    elif query.data == 'criteria_button':
        criteria_text = (
            "Критерии клана DEKTRIAN FAMILY:\n"
            "1. Смена тега в течение 7 дней.\n"
            "2. КД на 100 матчей: девушки - 4; мужчины - 5.\n"
            "3. Возраст 16+.\n"
            "4. Актив в чате Telegram.\n"
            "5. Участие в стримах лидера и мероприятиях клана.\n\n"
            "Критерии клана DEKTRIAN ACADEMY:\n"
            "1. Смена тега в течение 7 дней.\n"
            "2. КД и матчи не важны.\n"
            "3. Возраст 14+.\n"
            "4. Актив в чате.\n"
            "5. Участие в мероприятиях.\n\n"
            "Критерии DEKTRIAN ESPORTS:\n"
            "1. Возраст 16+.\n"
            "2. Наличие хайлайтов и результатов.\n"
            "3. Приоритет - собранные команды."
        )
        await query.message.edit_text(criteria_text, reply_markup=get_buttons())
    elif query.data == 'admins_button':
        admins_text = "Список админов клана:\n" + "\n".join(ADMINS)
        await query.message.edit_text(admins_text, reply_markup=get_buttons())
    return

# Основная функция
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            READY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ready)],
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nickname)],
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_id)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            KD_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_current)],
            KD_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_previous)],
            MATCHES_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_current)],
            MATCHES_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_previous)],
            SCREENSHOT_1: [MessageHandler(filters.PHOTO, screenshot_1)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO, screenshot_2)],
        },
        fallbacks=[]
    )

    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(conversation_handler)

    port = int(os.environ.get("PORT", 10000))

    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == '__main__':
    main()
