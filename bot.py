from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2 = range(11)

# Функция для создания кнопок "Отмена", "Критерии" и "Админы"
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data='reset')],
        [InlineKeyboardButton("Критерии", callback_data='criteria')],
        [InlineKeyboardButton("Админы", callback_data='admins')]  # Кнопка для отображения админов
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
        await update.message.reply_text("Отлично! Напиши свой игровой никнейм.")
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("Если передумаешь, напиши 'да'.")
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.")
        return READY

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь, пожалуйста, укажи свой игровой айди.",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text(
        "Сколько тебе полных лет?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        "Ты девочка или парень?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return GENDER

# Получение пола
async def gender(update: Update, context: CallbackContext) -> int:
    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text(
        "Какая у тебя КД за текущий сезон?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return KD_CURRENT

# Получение КД за текущий сезон
async def kd_current(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text(
        "Какой у тебя КД за прошлый сезон?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return KD_PREVIOUS

# Получение КД за прошлый сезон
async def kd_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в текущем сезоне?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return MATCHES_CURRENT

# Получение матчей за текущий сезон
async def matches_current(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в прошлом сезоне?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return MATCHES_PREVIOUS

# Получение матчей за прошлый сезон
async def matches_previous(update: Update, context: CallbackContext) -> int:
    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text(
        "Пожалуйста, отправь скриншот статистики из игры за текущий сезон.",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return SCREENSHOT_1

# Получение первого скриншота
async def screenshot_1(update: Update, context: CallbackContext) -> int:
    # Проверяем, если сообщение содержит фото
    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id  # Сохраняем первый скриншот
        await update.message.reply_text(
            "Теперь отправь скриншот статистики из игры за прошлый сезон.",
            reply_markup=get_buttons()  # Добавляем кнопки
        )
        return SCREENSHOT_2  # Переходим к следующему шагу, ожидая второй скриншот
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.")
        return SCREENSHOT_1  # Ожидаем повторно скриншот

# Получение второго скриншота
async def screenshot_2(update: Update, context: CallbackContext) -> int:
    # Проверяем, если сообщение содержит фото
    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id  # Сохраняем второй скриншот
        
        # Получаем юзернейм и айди пользователя Telegram
        telegram_username = update.message.from_user.username
        telegram_user_id = update.message.from_user.id        
        
        # Формируем заявку
        application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                      f"Игровой ник: {context.user_data['nickname']}\n" \
                      f"Игровой айди: {context.user_data['player_id']}\n" \
                      f"Возраст: {context.user_data['age']}\n" \
                      f"Пол: {context.user_data['gender']}\n" \
                      f"КД за текущий сезон: {context.user_data['kd_current']}\n" \
                      f"Матчи в текущем сезоне: {context.user_data['matches_current']}\n" \
                      f"КД за прошлый сезон: {context.user_data['kd_previous']}\n" \
                      f"Матчи в прошлом сезоне: {context.user_data['matches_previous']}\n" \
                      f"Telegram Username: @{telegram_username}\n" \
                      f"Telegram UserID: {telegram_user_id}\n"  # Добавляем Telegram юзернейм и айди

        # Отправляем заявку админу и группе
        try:
            await context.bot.send_message(ADMIN_ID, application)
            await context.bot.send_message(GROUP_ID, application)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке сообщения: {e}")

        # Отправка скриншотов
        try:
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_2'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_2'])
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке скриншотов: {e}")

        # Уведомление для пользователя
        await update.message.reply_text(
            "Ваша заявка отправлена, ожидайте ответ в течении дня! Если что-то не получилось или появились дополнительные вопросы, то напишите Лидеру клана @DektrianTV.",
            reply_markup=get_buttons()  # Добавляем кнопки
        )
        
    return ConversationHandler.END

# Функция для сброса данных
async def reset(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()  # Очищаем все данные пользователя
    await update.callback_query.message.edit_text(
        "Все данные были сброшены. Начни процесс подачи заявки заново, введя свой игровой никнейм!",
        reply_markup=get_buttons()  # Кнопка сброса
    )
    # Вернуться в состояние NICKNAME для повторного ввода данных
    return NICKNAME

# Функция для обработки нажатия на кнопку сброса и критериев
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'reset':  # Проверяем callback_data
        # Выполняем сброс данных
        return await reset(update, context)
    elif query.data == 'criteria':  # Кнопка для показа критериев
        criteria_text = (
            "Критерии клана DEKTRIAN FAMILY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд на 100 матчей (Девушки - 4; Мужчины - 5)\n"
            "3. Возраст 16+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "Критерии клана DEKTRIAN ACADEMY:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Кд и матчи не важны.\n"
            "3. Возраст 14+.\n"
            "4. Актив в телеграмм чате.\n"
            "5. Участие на стримах Лидера и клановых мероприятиях.\n\n"
            "Критерии клана DEKTRIAN ESPORTS:\n"
            "1. Смена тега в течении 7 дней.\n"
            "2. Возраст 16+\n"
            "3. Наличие результатов и хайлайтов\n"
            "4. Преемущество отдается собранным пакам\n"            
        )
        await query.message.edit_text(criteria_text, reply_markup=get_buttons())  # Показываем критерии с кнопками
    elif query.data == 'admins':  # Кнопка для показа списка админов
        admins_text = "Список админов клана DEKTRIAN FAMILY:\n" \
                      "1. Лидер клана - @DektrianTV\n" \
                      "2. Заместитель - @Admin1\n" \
                      "3. Модератор - @Admin2\n" \
                      "4. Модератор - @Admin3\n"
        await query.message.edit_text(admins_text, reply_markup=get_buttons())  # Показываем список админов
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
