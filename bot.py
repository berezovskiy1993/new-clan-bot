from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора и группы
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843
GROUP_ID = -1002640250280

# Этапы анкеты
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, MATCHES_CURRENT, SCREENSHOT_1, KD_PREVIOUS, MATCHES_PREVIOUS, SCREENSHOT_2 = range(11)

# Админы
ADMINS = ["@DektrianTV - Лидер всех кланов", "@Ffllooffy - Зам основы и Лидер Еспортс", "@neverforgotme - Лидер Академки", "@Vasvyu6 - Зам Академки"]

# Кнопки внизу анкеты

def get_buttons():
    keyboard = [[
        InlineKeyboardButton("Меню", callback_data='menu'),
        InlineKeyboardButton("Отмена", callback_data='reset_button')
    ]]
    return InlineKeyboardMarkup(keyboard)

# Меню

def get_menu_buttons():
    keyboard = [
        [InlineKeyboardButton("Критерии", callback_data='criteria_button')],
        [InlineKeyboardButton("Админы", callback_data='admins_button')],
        [InlineKeyboardButton("Соцсети", callback_data='socials_button')],
        [InlineKeyboardButton("⬅ Назад", callback_data='back_button')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Соцсети как кнопки

def get_social_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("YouTube", url="https://www.youtube.com/@Dektrian_TV")],
        [InlineKeyboardButton("Twitch", url="https://www.twitch.tv/dektrian_tv")],
        [InlineKeyboardButton("Группа Telegram", url="https://t.me/dektrian_tv")],
        [InlineKeyboardButton("Канал Telegram", url="https://t.me/dektrian_family")],
        [InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@dektrian_tv")],
        [InlineKeyboardButton("⬅ Назад", callback_data='back_button')],
    ])

# Обработка команды /start
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "*Привет\! Я бот клана DEKTRIAN FAMILY\! Если готовы подать заявку на вступление в клан — напишите 'да' или 'нет'.*",
        parse_mode="MarkdownV2",
        reply_markup=get_buttons()
    )
    return READY

# Этап "готов"
async def ready(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text.lower()
    if user_response == 'да':
        await update.message.reply_text("*Отлично\! Напиши свой игровой никнейм\.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("*Если передумаешь, напиши 'да'.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
        return READY
    else:
        await update.message.reply_text("*Пожалуйста, ответь 'да' или 'нет'.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
        return READY

# Остальные этапы — аналогично

async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text("*Теперь укажи свой игровой айди.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return PLAYER_ID

async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text("*Сколько тебе полных лет?*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return AGE

async def age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text("*Ты девочка или парень?*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return GENDER

async def gender(update: Update, context: CallbackContext) -> int:
    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text("*Какой у тебя КД за текущий сезон?*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return KD_CURRENT

async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text("*Сколько матчей ты сыграл в текущем сезоне?*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return MATCHES_CURRENT

async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text("*Отправь скриншот статистики за текущий сезон.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return SCREENSHOT_1

async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id
        await update.message.reply_text("*Теперь укажи КД за прошлый сезон.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
        return KD_PREVIOUS
    else:
        await update.message.reply_text("*Пожалуйста, отправьте скриншот.*", parse_mode="MarkdownV2")
        return SCREENSHOT_1

async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text("*Сколько матчей ты сыграл в прошлом сезоне?*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return MATCHES_PREVIOUS

async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text("*Теперь отправь скриншот за прошлый сезон.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
    return SCREENSHOT_2

async def screenshot_2(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id
        username = update.message.from_user.username
        user_id = update.message.from_user.id

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
            f"Telegram Username: @{username}\n"
            f"Telegram UserID: {user_id}\n"
        )

        await context.bot.send_message(ADMIN_ID, application)
        await context.bot.send_message(GROUP_ID, application)
        await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_1'])
        await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_2'])
        await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_1'])
        await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_2'])

        await update.message.reply_text(
            "*Ваша заявка отправлена, ожидайте ответ в течение дня\! Если появились вопросы — напишите Лидеру @DektrianTV\.*",
            parse_mode="MarkdownV2",
            reply_markup=get_buttons()
        )
    return ConversationHandler.END

# Обработка меню
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'reset_button':
        context.user_data.clear()
        await query.message.edit_text("*Все данные сброшены\. Начни сначала — введи никнейм\.*", parse_mode="MarkdownV2", reply_markup=get_buttons())
        return NICKNAME
    elif query.data == 'menu':
        await query.message.edit_reply_markup(reply_markup=get_menu_buttons())
    elif query.data == 'back_button':
        await query.message.edit_reply_markup(reply_markup=get_buttons())
    elif query.data == 'criteria_button':
        await query.message.edit_text(
            "*Критерии клана DEKTRIAN FAMILY:*\n1\. Смена тега в течении 7 дней\.\n2\. КД: \(Девушки\) 4 \| \(Мужчины\) 5\n3\. Возраст: 16\+\n4\. Актив в чате\n5\. Участие на стримах\n\n"
            "*DEKTRIAN ACADEMY:*\n1\. Смена тега за 7 дней\n2\. Возраст 14\+\n3\. Остальное не важно\n\n"
            "*DEKTRIAN ESPORTS:*\n1\. Тег\, возраст 16\+\n2\. Хайлайты и пак\n",
            parse_mode="MarkdownV2",
            reply_markup=get_menu_buttons()
        )
    elif query.data == 'admins_button':
        await query.message.edit_text("*Список админов:*\n" + '\n'.join(ADMINS), parse_mode="MarkdownV2", reply_markup=get_menu_buttons())
    elif query.data == 'socials_button':
        await query.message.edit_text("*Соцсети клана и его лидера:*", parse_mode="MarkdownV2", reply_markup=get_social_buttons())

# Запуск

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            READY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ready), CallbackQueryHandler(button_callback)],
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nickname)],
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_id)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            KD_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_current)],
            MATCHES_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_current)],
            SCREENSHOT_1: [MessageHandler(filters.PHOTO, screenshot_1)],
            KD_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_previous)],
            MATCHES_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_previous)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO, screenshot_2)],
        },
        fallbacks=[]
    )

    application.add_handler(conversation_handler)
    application.add_handler(CallbackQueryHandler(button_callback))

    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == '__main__':
    main()
