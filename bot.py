from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2 = range(11)

# Функция для создания кнопок "Критерии"
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Критерии", callback_data='criteria')],
        [InlineKeyboardButton("Начать заново", callback_data='restart')]  # Кнопка "Начать заново"
    ]
    return InlineKeyboardMarkup(keyboard)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    # Отправляем приветственное сообщение и картинку
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",  # Ссылка на картинку
        caption=" "  # Подпись под картинкой
    )
    await update.message.reply_text(
        "Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан - напишите 'да' или 'нет'.",
        reply_markup=get_buttons()  # Добавляем кнопки "Критерии" и "Начать заново"
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

# Остальные функции получения данных (nickname, player_id, age и т.д.)
# ...

# Функция для обработки нажатия на кнопку "Критерии"
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'criteria':
        # Показ критериев клана
        criteria_text = (
            "Критерии клана DEKTRIAN FAMILY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. КД на 100 матчей (Девушки - 4; Мужчины - 5)\n"
            "3. Возраст 16+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "Критерии клана DEKTRIAN ACADEMY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. КД и матчи не важны.\n"
            "3. Возраст 14+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "Критерии клана DEKTRIAN ESPORTS:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Возраст 16+\n"
            "3. Наличие результатов и хайлайтов\n"
            "4. Преимущество отдается собранным пакам\n"
        )
        await query.message.edit_text(criteria_text, reply_markup=get_buttons())  # Показываем критерии с кнопками
    elif query.data == 'restart':
        # Функция для начала процесса заново
        context.user_data.clear()  # Очищаем все данные пользователя
        await query.message.edit_text("Давай начнем с самого начала! Напиши 'да' для подачи заявки.",
                                      reply_markup=get_buttons())  # Кнопки снова будут на экране
        return READY

# Функция для отмены
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

# Основная функция
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],  # точка начала
        states={
            READY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ready)],  # Ответ на 'да' или 'нет'
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nickname)],
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, player_id)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            KD_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_current)],
            KD_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, kd_previous)],
            MATCHES_CURRENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_current)],
            MATCHES_PREVIOUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, matches_previous)],  # Убедитесь, что это 9
            SCREENSHOT_1: [MessageHandler(filters.PHOTO, screenshot_1)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO, screenshot_2)],  # Новый шаг для второго скриншота
        },
        fallbacks=[CommandHandler('cancel', cancel)]  # Обработчик для команды отмены
    )

    # Обработчик коллбэков для кнопок
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
