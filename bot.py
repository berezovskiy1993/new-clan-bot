from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES = range(5)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Если хочешь подать заявку на вступление в клан, то отправь любой символ в чат!")
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
    
    # Получаем ссылку на профиль пользователя
    user = update.message.from_user
    if user.username:
        user_link = f"@{user.username}"  # Ссылка на профиль через username
    else:
        user_link = f"[Профиль](tg://user?id={user.id})"  # Ссылка через user.id

    # Создаём сообщение с заявкой
    application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                  f"Игровой ник: {context.user_data['nickname']}\n" \
                  f"Игровой айди: {context.user_data['player_id']}\n" \
                  f"Возраст: {context.user_data['age']}\n" \
                  f"КД за два сезона: {context.user_data['kd']}\n" \
                  f"Матчи в этом и прошлом сезоне: {context.user_data['matches']}\n" \
                  f"Пользователь Telegram: {user_link}"
    
    # Отправляем заявку админу
    await context.bot.send_message(ADMIN_ID, application)

    # Уведомление для пользователя
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
