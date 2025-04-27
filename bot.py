import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ConversationHandler, ContextTypes, filters
)

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES = range(5)

# Стартовая функция
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Начать заявку", callback_data="start_application")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            "Привет! Я бот клана DEKTRIAN FAMILY. "
            "Хочешь вступить в наш клан? Нажми кнопку ниже!",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Привет! Я бот клана DEKTRIAN FAMILY. "
            "Хочешь вступить в наш клан? Нажми кнопку ниже!",
            reply_markup=reply_markup
        )
    
    return NICKNAME  # Ожидаем ввод никнейма

# Получение никнейма
async def nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        context.user_data['nickname'] = update.message.text
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_start")],
            [InlineKeyboardButton("Далее", callback_data="next_player_id")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Теперь введи свой игровой айди:", reply_markup=reply_markup)
        return PLAYER_ID
    return ConversationHandler.END

# Получение игрового ID
async def player_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not update.message.text.isdigit():
            await update.message.reply_text("Айди должен быть числом. Попробуй снова:")
            return PLAYER_ID
        context.user_data['player_id'] = update.message.text
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_nickname")],
            [InlineKeyboardButton("Далее", callback_data="next_age")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Теперь укажи свой возраст:", reply_markup=reply_markup)
        return AGE
    return ConversationHandler.END

# Получение возраста
async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not update.message.text.isdigit():
            await update.message.reply_text("Возраст должен быть числом. Попробуй снова:")
            return AGE
        context.user_data['age'] = update.message.text
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_player_id")],
            [InlineKeyboardButton("Далее", callback_data="next_kd")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Какая у тебя КД за последние два сезона?", reply_markup=reply_markup)
        return KD
    return ConversationHandler.END

# Получение КД
async def kd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not update.message.text.replace('.', '', 1).isdigit():
            await update.message.reply_text("КД должно быть числом. Попробуй снова:")
            return KD
        context.user_data['kd'] = update.message.text
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back_age")],
            [InlineKeyboardButton("Далее", callback_data="next_matches")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Сколько матчей ты сыграл за последние два сезона?", reply_markup=reply_markup)
        return MATCHES
    return ConversationHandler.END

# Получение количества матчей
async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if not update.message.text.isdigit():
            await update.message.reply_text("Количество матчей должно быть числом. Попробуй снова:")
            return MATCHES
        context.user_data['matches'] = update.message.text

        user = update.message.from_user
        if user.username:
            user_link = f"@{user.username}"
        else:
            user_link = f"[Профиль](tg://user?id={user.id})"

        application_text = (
            "📥 Новая заявка в клан DEKTRIAN FAMILY:\n\n"
            f"👤 Telegram: {user_link}\n"
            f"🎮 Никнейм: {context.user_data['nickname']}\n"
            f"🆔 Игровой ID: {context.user_data['player_id']}\n"
            f"🎂 Возраст: {context.user_data['age']}\n"
            f"⚔️ КД за 2 сезона: {context.user_data['kd']}\n"
            f"🏆 Матчей за 2 сезона: {context.user_data['matches']}"
        )

        # Отправляем админу заявку
        await context.bot.send_message(ADMIN_ID, application_text, parse_mode="Markdown")
        await update.message.reply_text("✅ Ваша заявка успешно отправлена! Ожидайте ответа администратора.")
        return ConversationHandler.END
    return ConversationHandler.END

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start_application":
        await query.message.reply_text("Отправь свой игровой никнейм:")
        return NICKNAME
    elif data == "next_player_id":
        await query.message.reply_text("Отправь свой игровой айди:")
        return PLAYER_ID
    elif data == "next_age":
        await query.message.reply_text("Отправь свой возраст:")
        return AGE
    elif data == "next_kd":
        await query.message.reply_text("Укажи свою КД за два сезона:")
        return KD
    elif data == "next_matches":
        await query.message.reply_text("Сколько матчей сыграл за последние два сезона?")
        return MATCHES
    elif data == "back_start":
        return await start(update, context)
    elif data == "back_nickname":
        await query.message.reply_text("Вернись к вводу никнейма:")
        return NICKNAME
    elif data == "back_player_id":
        await query.message.reply_text("Вернись к вводу айди:")
        return PLAYER_ID
    elif data == "back_age":
        await query.message.reply_text("Вернись к вводу возраста:")
        return AGE
    else:
        await query.message.reply_text("Неизвестная команда.")
        return ConversationHandler.END

# Основная функция
def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NICKNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, nickname),
                CallbackQueryHandler(button)
            ],
            PLAYER_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, player_id),
                CallbackQueryHandler(button)
            ],
            AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, age),
                CallbackQueryHandler(button)
            ],
            KD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, kd),
                CallbackQueryHandler(button)
            ],
            MATCHES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, matches),
                CallbackQueryHandler(button)
            ],
        },
        fallbacks=[CallbackQueryHandler(button)],
        per_message=True,
    )

    application.add_handler(conv_handler)

    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",
    )

if __name__ == '__main__':
    main()
