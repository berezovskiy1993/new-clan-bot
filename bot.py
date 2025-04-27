from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Укажите свой токен
TOKEN = 'YOUR_BOT_TOKEN'

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES = range(5)

# Администратор и другие пользователи
admin_id = 'ADMIN_USER_ID'  # ID администратора
user_ids = ['USER_ID_1', 'USER_ID_2']  # Другие пользователи

# Стартовая функция
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Хочешь вступить в наш клан? Пожалуйста, отправь заявку!")
    return NICKNAME

# Получение никнейма
def nickname(update: Update, context: CallbackContext):
    context.user_data['nickname'] = update.message.text
    update.message.reply_text("Отлично! Теперь, пожалуйста, укажи свой игровой айди.")
    return PLAYER_ID

# Получение игрового ID
def player_id(update: Update, context: CallbackContext):
    context.user_data['player_id'] = update.message.text
    update.message.reply_text("Теперь укажи свой возраст.")
    return AGE

# Получение возраста
def age(update: Update, context: CallbackContext):
    context.user_data['age'] = update.message.text
    update.message.reply_text("Какая у тебя КД за последние два сезона?")
    return KD

# Получение КД
def kd(update: Update, context: CallbackContext):
    context.user_data['kd'] = update.message.text
    update.message.reply_text("Сколько матчей ты сыграл в этом и прошлом сезоне?")
    return MATCHES

# Получение матчей
def matches(update: Update, context: CallbackContext):
    context.user_data['matches'] = update.message.text
    
    # Создаём сообщение с заявкой
    application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                  f"Игровой ник: {context.user_data['nickname']}\n" \
                  f"Игровой айди: {context.user_data['player_id']}\n" \
                  f"Возраст: {context.user_data['age']}\n" \
                  f"КД за два сезона: {context.user_data['kd']}\n" \
                  f"Матчи в этом и прошлом сезоне: {context.user_data['matches']}"
    
    # Отправляем заявку администратору и другим пользователям
    context.bot.send_message(admin_id, application)
    for user_id in user_ids:
        context.bot.send_message(user_id, application)

    update.message.reply_text("Ваша заявка отправлена! Спасибо, что подали её!")
    return ConversationHandler.END

# Функция для отмены
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

# Основная функция
def main():
    # Создаем Updater и передаем токен
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Создаем ConversationHandler для сбора данных
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NICKNAME: [MessageHandler(Filters.text & ~Filters.command, nickname)],
            PLAYER_ID: [MessageHandler(Filters.text & ~Filters.command, player_id)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            KD: [MessageHandler(Filters.text & ~Filters.command, kd)],
            MATCHES: [MessageHandler(Filters.text & ~Filters.command, matches)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем ConversationHandler в диспетчер
    dispatcher.add_handler(conversation_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
