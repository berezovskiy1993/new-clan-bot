from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES = range(5)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Начать заявку", callback_data="start_application")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Хочешь вступить в наш клан? Пожалуйста, отправь заявку!", reply_markup=reply_markup)
    return NICKNAME

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="back_start")],
        [InlineKeyboardButton("Далее", callback_data="next_player_id")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Отлично! Теперь, пожалуйста, укажи свой игровой айди.", reply_markup=reply_markup)
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("Айди должен состоять только из чисел. Пожалуйста, попробуй снова.")
        return PLAYER_ID
    
    context.user_data['player_id'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="back_nickname")],
        [InlineKeyboardButton("Далее", callback_data="next_age")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Теперь укажи свой возраст.", reply_markup=reply_markup)
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("Возраст должен быть числом. Пожалуйста, попробуй снова.")
        return AGE

    context.user_data['age'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="back_player_id")],
        [InlineKeyboardButton("Далее", callback_data="next_kd")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Какая у тебя КД за последние два сезона?", reply_markup=reply_markup)
    return KD

# Получение КД
async def kd(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("КД должно быть числом. Пожалуйста, попробуй снова.")
        return KD

    context.user_data['kd'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="back_age")],
        [InlineKeyboardButton("Далее", callback_data="next_matches")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Сколько матчей ты сыграл в этом и прошлом сезоне?", reply_markup=reply_markup)
    return MATCHES

# Получение матчей
async def matches(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("Количество матчей должно быть числом. Пожалуйста, попробуй снова.")
        return MATCHES
    
    context.user_data['matches'] = update.message.text

    # Создаём сообщение с заявкой
    application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                  f"Игровой ник: {context.user_data['nickname']}\n" \
                  f"Игровой айди: {context.user_data['player_id']}\n" \
                  f"Возраст: {context.user_data['age']}\n" \
                  f"КД за два сезона: {context.user_data['kd']}\n" \
                  f"Матчи в этом и прошлом сезоне: {context.user_data['matches']}"
    
    # Отправляем заявку только админу
    await context.bot.send_message(ADMIN_ID, application)

    await update.message.reply_text("Ваша заявка отправлена! Спасибо, что подали её!")
    return ConversationHandler.END

# Функция возврата на предыдущий шаг
async def back_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Заявка отменена. Начнем сначала.")
    return start(update, context)

async def back_nickname(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Возвращаемся к вводу никнейма.")
    return NICKNAME

async def back_player_id(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Возвращаемся к вводу айди.")
    return PLAYER_ID

async def back_age(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Возвращаемся к вводу возраста.")
    return AGE

# Обработчики нажатий кнопок
async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = query.data
    if data == "start_application":
        return await nickname(update, context)
    elif data == "next_player_id":
        return await player_id(update, context)
    elif data == "next_age":
        return await age(update, context)
    elif data == "next_kd":
        return await kd(update, context)
    elif data == "next_matches":
        return await matches(update, context)
    elif data == "back_start":
        return await back_start(update, context)
    elif data == "back_nickname":
        return await back_nickname(update, context)
    elif data == "back_player_id":
        return await back_player_id(update, context)
    elif data == "back_age":
        return await back_age(update, context)

# Основная функция
def main() -> None:
    # Создаем Application и передаем токен
    application = Application.builder().token(TOKEN).build()

    # Создаем ConversationHandler для сбора данных
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nickname)],
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_id)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            KD: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd)],
            MATCHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches)],
        },
        fallbacks=[CallbackQueryHandler(button)],  # Используем CallbackQueryHandler для обработки нажатий кнопок
    )

    # Добавляем ConversationHandler в приложение
    application.add_handler(conversation_handler)

    # Получаем порт из переменной окружения (на Render это будет порт 10000)
    port = int(os.environ.get("PORT", 10000))

    # Настройка вебхука
    application.run_webhook(
        listen="0.0.0.0",  # Слушаем все IP
        port=port,  # Порт, на котором сервер будет слушать
        url_path=TOKEN,  # URL-часть для вебхука
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}",  # Полный URL вебхука
    )

if __name__ == '__main__':
    main()
