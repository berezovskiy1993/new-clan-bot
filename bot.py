from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES = range(5)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Хочешь вступить в наш клан? Пожалуйста, отправь заявку!")
    return NICKNAME

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text("Отлично! Теперь, пожалуйста, укажи свой игровой айди.")
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text("Теперь укажи свой возраст.")
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text("Какая у тебя КД за последние два сезона?")
    return KD

# Получение КД
async def kd(update: Update, context: CallbackContext) -> int:
    context.user_data['kd'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в этом и прошлом сезоне?")
    return MATCHES

# Получение матчей
async def matches(update: Update, context: CallbackContext) -> int:
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

# Функция для отмены
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

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
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем ConversationHandler в приложение
    application.add_handler(conversation_handler)

    # Запускаем бота без asyncio.run()
    application.run_polling()

if __name__ == '__main__':
    main()
