from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора
GROUP_ID = -1002640250280  # ID закрытой группы

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2 = range(11)

# Список админов клана
ADMINS = ["@Admin1", "@Admin2", "@Admin3"]  # Замените на реальные никнеймы админов

# Функция для создания кнопок
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("Меню", callback_data='menu')],
        [InlineKeyboardButton("Отмена", callback_data='reset')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_photo(
        photo="https://ibb.co/JRbbTWsQ",  # Ссылка на картинку
        caption=" "  # Подпись под картинкой
    )
    await update.message.reply_text(
        "Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан - напишите 'да' или 'нет'.",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return READY

# Проверка на готовность подать заявку
async def ready(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

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
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь, пожалуйста, укажи свой игровой айди.",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['player_id'] = update.message.text
    await update.message.reply_text(
        "Сколько тебе полных лет?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        "Ты девочка или парень?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return GENDER

# Получение пола
async def gender(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text(
        "Какая у тебя КД за текущий сезон?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return KD_CURRENT

# Получение КД за текущий сезон
async def kd_current(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text(
        "Какой у тебя КД за прошлый сезон?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return KD_PREVIOUS

# Получение КД за прошлый сезон
async def kd_previous(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в текущем сезоне?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return MATCHES_CURRENT

# Получение матчей за текущий сезон
async def matches_current(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text(
        "Сколько матчей ты сыграл в прошлом сезоне?",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return MATCHES_PREVIOUS

# Получение матчей за прошлый сезон
async def matches_previous(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text(
        "Пожалуйста, отправь скриншот статистики из игры за текущий сезон.",
        reply_markup=get_buttons()  # Добавляем кнопки
    )
    return SCREENSHOT_1

# Получение первого скриншота
async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

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
    if update.callback_query and update.callback_query.data == 'reset':
        return await reset(update, context)  # Если нажата кнопка "Отмена", сбрасываем данные

    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id  # Сохраняем второй скриншот

        # Формируем заявку
        application = f"Заявка на вступление в клан DEKTRIAN FAMILY:\n" \
                      f"Игровой ник: {context.user_data['nickname']}\n" \
                      f"Игровой айди: {context.user_data['player_id']}\n" \
                      f"Возраст: {context.user_data['age']}\n" \
                      f"Пол: {context.user_data['gender']}\n" \
                      f"КД за текущий сезон: {context.user_data['kd_current']}\n" \
                      f"Матчи в текущем сезоне: {context.user_data['matches_current']}\n" \
                      f"КД за прошлый сезон: {context.user_data['kd_previous']}\n" \
                      f"Матчи в прошлом сезоне: {context.user_data['matches_previous']}\n"

        try:
            await context.bot.send_message(ADMIN_ID, application)
            await context.bot.send_message(GROUP_ID, application)
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке сообщения: {e}")

        try:
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(ADMIN_ID, photo=context.user_data['screenshot_2'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_1'])
            await context.bot.send_photo(GROUP_ID, photo=context.user_data['screenshot_2'])
        except Exception as e:
            await update.message.reply_text(f"Ошибка при отправке скриншотов: {e}")

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
    await update.message.reply_text("Отмена")  # Сообщение об отмене
    return NICKNAME  # Возвращаем пользователя на ввод никнейма

# Функция для обработки нажатия на кнопку сброса, меню, критериев и админов
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'reset':  # Проверяем callback_data
        return await reset(update, context)
    elif query.data == 'menu':
        await query.message.edit_text("Выберите действие:", reply_markup=get_buttons())
    return

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
            SCREENSHOT_1: [MessageHandler(filters.PHOTO, screenshot_1)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO, screenshot_2)],
        },
        fallbacks=[]
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
