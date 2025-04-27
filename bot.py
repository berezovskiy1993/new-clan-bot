from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS = range(8)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Если хочешь подать заявку на вступление в клан - для начала напиши свой игровой никнейм!")
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
    await update.message.reply_text("Ты девочка или парень? Напиши 'девочка' или 'парень'.")
    return GENDER

# Получение пола
async def gender(update: Update, context: CallbackContext) -> int:
    gender = update.message.text.lower()
    if gender not in ['девочка', 'парень']:
        await update.message.reply_text("Пожалуйста, напиши 'девочка' или 'парень'.")
        return GENDER
    context.user_data['gender'] = gender
    await update.message.reply_text("Какая у тебя КД за текущий сезон?")
    return KD_CURRENT

# Получение КД за текущий сезон
async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text("А какая у тебя КД за прошлый сезон?")
    return KD_PREVIOUS

# Получение КД за прошлый сезон
async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в текущем сезоне?")
    return MATCHES_CURRENT

# Получение матчей за текущий сезон
async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в прошлом сезоне?")
    return MATCHES_PREVIOUS

# Получение матчей за прошлый сезон
async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    
    # Получаем данные о пользователе
    user = update.message.from_user
    
    # Формирование ссылки на профиль пользователя (с помощью ID, который кликабелен)
    user_id_link = f"tg://user?id={user.id}"  # Ссылка через user.id (будет работать в мобильном приложении)
    
    # Получение юзернейма
    username = user.username if user.username else "Не указан"

    # Создаём сообщение с заявкой
    application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                  f"Игровой ник: {context.user_data['nickname']}\n" \
                  f"Игровой айди: {context.user_data['player_id']}\n" \
                  f"Возраст: {context.user_data['age']}\n" \
                  f"Пол: {context.user_data['gender']}\n" \
                  f"КД за текущий сезон: {context.user_data['kd_current']}\n" \
                  f"КД за прошлый сезон: {context.user_data['kd_previous']}\n" \
                  f"Матчи в текущем сезоне: {context.user_data['matches_current']}\n" \
                  f"Матчи в прошлом сезоне: {context.user_data['matches_previous']}\n" \
                  f"Пользователь Telegram (ID): [Профиль]({user_id_link})\n" \
                  f"Юзернейм: @{username}"

    # Отправляем заявку админу
    try:
        await context.bot.send_message(ADMIN_ID, application)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при отправке сообщения админу: {e}")

    # Отправляем заявку в закрытую группу
    try:
        await context.bot.send_message(GROUP_ID, application)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при отправке сообщения в группу: {e}")

    # Уведомление для пользователя
    await update.message.reply_text("Ваша заявка отправлена, Спасибо! Если что-то не получилось или появились дополнительные вопросы, то напишите Лидеру клана @DektrianTV.")
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
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            KD_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_current)],
            KD_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_previous)],
            MATCHES_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_current)],
            MATCHES_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_previous)],
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
