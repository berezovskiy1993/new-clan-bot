from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2 = range(11)

# Функция для создания кнопок "Админы"
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Админы", callback_data='admins')],
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
        reply_markup=get_buttons()  # Добавляем две кнопки
    )
    return READY

# Проверка на готовность подать заявку
async def ready(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text.lower()
    if user_response == 'да':
        await update.message.reply_text("Отлично! Напиши свой игровой никнейм.", reply_markup=get_buttons())
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("Если передумаешь, напиши 'да'.", reply_markup=get_buttons())
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.", reply_markup=get_buttons())
        return READY

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nНикнейм: {context.user_data['nickname']}", reply_markup=get_buttons())
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nИгровой айди: {context.user_data['player_id']}", reply_markup=get_buttons())
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nВозраст: {context.user_data['age']}", reply_markup=get_buttons())
    return GENDER

# Получение пола
async def gender(update: Update, context: CallbackContext) -> int:
    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text(f"Правильно ли введены данные?\nПол: {context.user_data['gender']}", reply_markup=get_buttons())
    return KD_CURRENT

# Получение КД за текущий сезон
async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nКД за текущий сезон: {context.user_data['kd_current']}", reply_markup=get_buttons())
    return KD_PREVIOUS

# Получение КД за прошлый сезон
async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nКД за прошлый сезон: {context.user_data['kd_previous']}", reply_markup=get_buttons())
    return MATCHES_CURRENT

# Получение матчей за текущий сезон
async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nМатчи в текущем сезоне: {context.user_data['matches_current']}", reply_markup=get_buttons())
    return MATCHES_PREVIOUS

# Получение матчей за прошлый сезон
async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text(f"Правильно ли введены данные?\nМатчи в прошлом сезоне: {context.user_data['matches_previous']}", reply_markup=get_buttons())
    return SCREENSHOT_1

# Получение первого скриншота
async def screenshot_1(update: Update, context: CallbackContext) -> int:
    # Проверяем, если сообщение содержит фото
    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id  # Сохраняем первый скриншот
        await update.message.reply_text(f"Правильно ли введены данные?\nСкриншот 1: {context.user_data['screenshot_1']}", reply_markup=get_buttons())
        return SCREENSHOT_2  # Переходим к следующему шагу, ожидая второй скриншот
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.", reply_markup=get_buttons())
        return SCREENSHOT_1  # Ожидаем повторно скриншот

# Получение второго скриншота
async def screenshot_2(update: Update, context: CallbackContext) -> int:
    # Проверяем, если сообщение содержит фото
    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id  # Сохраняем второй скриншот
        await update.message.reply_text("Ваша заявка отправлена, ожидайте ответ в течении дня!")
    return ConversationHandler.END

# Функция для обработки нажатия на кнопку "Админы"
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'admins':  # Кнопка для показа админов
        admins_list = "Админы клана DEKTRIAN FAMILY:\n- Админ 1\n- Админ 2\n- Админ 3"  # Пример списка админов
        await query.message.edit_text(admins_list, reply_markup=get_buttons())  # Показываем список админов
    return

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
        fallbacks=[]  # Если нужно обработать ошибки или завершение процесса
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
