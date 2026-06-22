import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Загружаем переменные окружения (только через Render)
TOKEN = os.environ.get("API_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
GROUP_ID = -1002640250280  # основная группа для заявок
EXTRA_GROUP_ID = -1002011191845  # дополнительная группа, куда тоже отправляется заявка

# Этапы анкеты
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, MATCHES_CURRENT, SCREENSHOT_1, KD_PREVIOUS, MATCHES_PREVIOUS, SCREENSHOT_2 = range(11)

# Список админов
ADMINS = [
    "@DektrianTV - Лидер всех кланов",
    "@D13Alastor - Лидер Основы",
    "@Angel_of_rain - Зам Основы",
    "@FRUKTIK58 - Зам Основы",
    "@D13_cocomber - Лидер Академки",   
]

# Кнопки "Меню" и "Сначала"
def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Меню", callback_data='menu'),
         InlineKeyboardButton("Сначала", callback_data='reset_button')]
    ])

def get_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Критерии", callback_data='criteria_button')],
        [InlineKeyboardButton("Админы", callback_data='admins_button')],
        [InlineKeyboardButton("Соцсети", callback_data='socials_button')],
        [InlineKeyboardButton("⬅ Назад", callback_data='back_button')]
    ])

# Команда /start
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",
        caption=" "
    )
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Ты попал в бот клана DEKTRIAN FAMILY!\n"
        "Здесь ты можешь подать заявку в один из кланов:\n\n"
        "▫️ FAMILY — основной клан\n"      
        "▫️ ACADEMY — клан свободного стиля\n\n"
        "Напиши текстом 'да' и проходи анкету 📝\n\n",
        reply_markup=get_buttons()
    )
    return READY

# Ответ на "да" или "нет"
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

# Этапы анкеты
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data["nickname"] = update.message.text
    await update.message.reply_text("Теперь укажи свой игровой айди.", reply_markup=get_buttons())
    return PLAYER_ID

async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data["player_id"] = update.message.text
    await update.message.reply_text("Сколько тебе полных лет?", reply_markup=get_buttons())
    return AGE

async def age(update: Update, context: CallbackContext) -> int:
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Ты девочка или парень?", reply_markup=get_buttons())
    return GENDER

async def gender(update: Update, context: CallbackContext) -> int:
    context.user_data["gender"] = update.message.text.lower()
    await update.message.reply_text("Какой у тебя КД за текущий сезон?", reply_markup=get_buttons())
    return KD_CURRENT

async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data["kd_current"] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в текущем сезоне?", reply_markup=get_buttons())
    return MATCHES_CURRENT

async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data["matches_current"] = update.message.text
    await update.message.reply_text("Отправь скриншот статистики за текущий сезон.", reply_markup=get_buttons())
    return SCREENSHOT_1

async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data["screenshot_1"] = update.message.photo[-1].file_id
        await update.message.reply_text("Теперь укажи КД за прошлый сезон.", reply_markup=get_buttons())
        return KD_PREVIOUS
    await update.message.reply_text("Пожалуйста, отправьте скриншот.")
    return SCREENSHOT_1

async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data["kd_previous"] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в прошлом сезоне?", reply_markup=get_buttons())
    return MATCHES_PREVIOUS

async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data["matches_previous"] = update.message.text
    await update.message.reply_text("Теперь отправь скриншот за прошлый сезон.", reply_markup=get_buttons())
    return SCREENSHOT_2

# Финальный шаг — отправка анкеты и задержка
async def screenshot_2(update: Update, context: CallbackContext) -> int:
    if update.message.photo:
        context.user_data["screenshot_2"] = update.message.photo[-1].file_id
        u = update.message.from_user

        msg = (
            f"Заявка на вступление в клан DEKTRIAN FAMILY:\n"
            f"Игровой ник: {context.user_data['nickname']}\n"
            f"Игровой айди: {context.user_data['player_id']}\n"
            f"Возраст: {context.user_data['age']}\n"
            f"Пол: {context.user_data['gender']}\n"
            f"КД за текущий сезон: {context.user_data['kd_current']}\n"
            f"Матчи в текущем сезоне: {context.user_data['matches_current']}\n"
            f"КД за прошлый сезон: {context.user_data['kd_previous']}\n"
            f"Матчи в прошлом сезоне: {context.user_data['matches_previous']}\n"
            f"Telegram Username: @{u.username}\n"
            f"Telegram UserID: {u.id}\n"
        )

        try:
            await context.bot.send_message(ADMIN_ID, msg)
            await context.bot.send_photo(ADMIN_ID, context.user_data['screenshot_1'])
            await context.bot.send_photo(ADMIN_ID, context.user_data['screenshot_2'])

            await context.bot.send_message(GROUP_ID, msg)
            await context.bot.send_photo(GROUP_ID, context.user_data['screenshot_1'])
            await context.bot.send_photo(GROUP_ID, context.user_data['screenshot_2'])

            await context.bot.send_message(EXTRA_GROUP_ID, msg)
            await context.bot.send_photo(EXTRA_GROUP_ID, context.user_data['screenshot_1'])
            await context.bot.send_photo(EXTRA_GROUP_ID, context.user_data['screenshot_2'])

        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке: {e}")

        await update.message.reply_text("✅ Ваша заявка отправлена. Ожидайте ответ!", reply_markup=get_buttons())
        await asyncio.sleep(3)
        await update.message.reply_text("Хотите подать еще одну заявку? Напишите 'да' или 'нет'.", reply_markup=get_buttons())
        return READY

    await update.message.reply_text("Пожалуйста, отправьте скриншот.")
    return SCREENSHOT_2

# Сброс анкеты
async def reset(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.edit_text("Все введенные данные были сброшены! Напиши 'да' если готов начать заново.", reply_markup=get_buttons())                 
    return READY

# Обработка кнопок
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
            "2. Кд на 100 матчей (Девушки - 5; Мужчины - 7)\n"
            "3. Либо Кд Ультимейт (Девушки - 1.5; Мужчины - 2)\n"
            "4. Возраст 16+.\n"
            "5. Недельная энергия 500+.\n"
            "6. Актив в телеграмм чате.\n"
            "7. Участие на стримах Лидера и клановых мероприятиях.\n\n"            
            "_________________________________\n"
            "Критерии клана DEKTRIAN ACADEMY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд на 50 матчей (Девушки - 3; Мужчины - 3)\n"
            "3. Возраст 14+.\n"
            "4. Недельная энергия 300+.\n"
            "5. Актив в телеграмм чате.\n"
            "6. Участие на стримах Лидера и клановых мероприятиях.\n\n",
            reply_markup=get_menu_buttons()
        )
    elif query.data == 'admins_button':
        await query.message.edit_text("Список админов клана:\n" + "\n".join(ADMINS), reply_markup=get_menu_buttons())
    elif query.data == 'socials_button':
        await query.message.edit_text("Выберите платформу:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("YouTube", url="https://www.youtube.com/@Dektrian_TV")],
            [InlineKeyboardButton("Twitch", url="https://www.twitch.tv/dektrian_tv")],
            [InlineKeyboardButton("Группа Telegram", url="https://t.me/dektrian_tv")],
            [InlineKeyboardButton("Канал Telegram", url="https://t.me/dektrian_family")],
            [InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@dektrian_tv")],
            [InlineKeyboardButton("⬅ Назад", callback_data='back_button')]
        ]))

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()

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

    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == "__main__":
    main()
