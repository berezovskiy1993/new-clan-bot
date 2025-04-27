from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS = range(9)

# Функция для создания кнопок "Начать с начала" и "Критерии"
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Начать с начала", callback_data='reset')],
        [InlineKeyboardButton("Критерии", callback_data='criteria')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    # Прямая ссылка на изображение
    image_url = 'https://i.ibb.co/JRbbTWsQ/welcome-image.jpg'  # замените на ваш реальный URL

    # Отправка картинки с приветствием
    await update.message.reply_photo(
        photo=image_url,
        caption="Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан - напишите 'да' или 'нет'.",
        reply_markup=get_buttons()  # Добавляем две кнопки
    )
    return READY

# Проверка на готовность подать заявку
async def ready(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text.lower()
    if user_response == 'да':
        await update.message.reply_text("Напиши свой игровой никнейм.")
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("Если передумаешь, напиши 'да'.")
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.")
        return READY

# (дальше идет код с обработчиками для других состояний)

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
        },
        fallbacks=[CommandHandler('cancel', cancel), CallbackQueryHandler(button_callback)],
    )

    application.add_handler(conversation_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
