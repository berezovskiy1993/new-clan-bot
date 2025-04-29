from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843
GROUP_ID = -1002640250280

# Состояния для ConversationHandler
READY, NICKNAME, PLAYER_ID, AGE, GENDER, KD_CURRENT, KD_PREVIOUS, MATCHES_CURRENT, MATCHES_PREVIOUS, SCREENSHOT_1, SCREENSHOT_2, CANCELLED = range(12)

# Функции создания отдельных кнопок

def get_cancel_button():
    keyboard = [[InlineKeyboardButton("Отмена", callback_data='cancel')]]
    return InlineKeyboardMarkup(keyboard)

def get_criteria_button():
    keyboard = [[InlineKeyboardButton("Критерии", callback_data='criteria')]]
    return InlineKeyboardMarkup(keyboard)

def get_admins_button():
    keyboard = [[InlineKeyboardButton("Админы", callback_data='admins')]]
    return InlineKeyboardMarkup(keyboard)

def get_main_buttons():
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data='cancel')],
        [InlineKeyboardButton("Критерии", callback_data='criteria')],
        [InlineKeyboardButton("Админы", callback_data='admins')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Привет! Я бот клана DEKTRIAN FAMILY. Если готовы подать заявку на вступление в клан - напишите 'да' или 'нет'.",
        reply_markup=get_main_buttons()
    )
    return READY

# Проверка на готовность подать заявку
async def ready(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    user_response = update.message.text.lower()
    if user_response == 'да':
        await update.message.reply_text("Отлично! Напиши свой игровой никнейм.", reply_markup=get_main_buttons())
        return NICKNAME
    elif user_response == 'нет':
        await update.message.reply_text("Если передумаешь, напиши 'да'.", reply_markup=get_main_buttons())
        return READY
    else:
        await update.message.reply_text("Пожалуйста, ответь 'да' или 'нет'.", reply_markup=get_main_buttons())
        return READY

async def nickname(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['nickname'] = update.message.text
    await update.message.reply_text("Теперь укажи свой игровой ID.", reply_markup=get_main_buttons())
    return PLAYER_ID

async def player_id(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['player_id'] = update.message.text
    await update.message.reply_text("Сколько тебе полных лет?", reply_markup=get_main_buttons())
    return AGE

async def age(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['age'] = update.message.text
    await update.message.reply_text("Ты девочка или парень?", reply_markup=get_main_buttons())
    return GENDER

async def gender(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['gender'] = update.message.text.lower()
    await update.message.reply_text("Какая у тебя КД за текущий сезон?", reply_markup=get_main_buttons())
    return KD_CURRENT

async def kd_current(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['kd_current'] = update.message.text
    await update.message.reply_text("Какой КД у тебя был за прошлый сезон?", reply_markup=get_main_buttons())
    return KD_PREVIOUS

async def kd_previous(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['kd_previous'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в текущем сезоне?", reply_markup=get_main_buttons())
    return MATCHES_CURRENT

async def matches_current(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['matches_current'] = update.message.text
    await update.message.reply_text("Сколько матчей ты сыграл в прошлом сезоне?", reply_markup=get_main_buttons())
    return MATCHES_PREVIOUS

async def matches_previous(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    context.user_data['matches_previous'] = update.message.text
    await update.message.reply_text("Отправь скриншот за текущий сезон.", reply_markup=get_main_buttons())
    return SCREENSHOT_1

async def screenshot_1(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    if update.message.photo:
        context.user_data['screenshot_1'] = update.message.photo[-1].file_id
        await update.message.reply_text("Отправь скриншот за прошлый сезон.", reply_markup=get_main_buttons())
        return SCREENSHOT_2
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.", reply_markup=get_main_buttons())
        return SCREENSHOT_1

async def screenshot_2(update: Update, context: CallbackContext) -> int:
    if await check_cancel(update, context):
        return CANCELLED

    if update.message.photo:
        context.user_data['screenshot_2'] = update.message.photo[-1].file_id

        application_text = (
            f"Заявка на вступление:\n"
            f"Ник: {context.user_data['nickname']}\n"
            f"ID: {context.user_data['player_id']}\n"
            f"Возраст: {context.user_data['age']}\n"
            f"Пол: {context.user_data['gender']}\n"
            f"КД текущий: {context.user_data['kd_current']}\n"
            f"КД прошлый: {context.user_data['kd_previous']}\n"
            f"Матчи текущий: {context.user_data['matches_current']}\n"
            f"Матчи прошлый: {context.user_data['matches_previous']}\n"
        )

        await context.bot.send_message(ADMIN_ID, application_text)
        await context.bot.send_photo(ADMIN_ID, context.user_data['screenshot_1'])
        await context.bot.send_photo(ADMIN_ID, context.user_data['screenshot_2'])

        await update.message.reply_text("Заявка отправлена. Ожидайте ответа.", reply_markup=get_main_buttons())
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, отправьте скриншот.", reply_markup=get_main_buttons())
        return SCREENSHOT_2

# Обработка отмены
async def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    if update.callback_query:
        await update.callback_query.message.edit_text("Процесс отменён. Начни заново, если хочешь.", reply_markup=get_main_buttons())
    else:
        await update.message.reply_text("Процесс отменён. Начни заново, если хочешь.", reply_markup=get_main_buttons())
    return ConversationHandler.END

# Проверка отмены в сообщениях
async def check_cancel(update: Update, context: CallbackContext) -> bool:
    if update.message and update.message.text and update.message.text.lower() == "отмена":
        await cancel(update, context)
        return True
    return False

# Функция обработки нажатия кнопок
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'cancel':
        await cancel(update, context)
    elif query.data == 'criteria':
        await query.message.edit_text("Критерии вступления:\n- КД 4-5+\n- 16+ лет\n- Активность\n- Участие в стримах", reply_markup=get_main_buttons())
    elif query.data == 'admins':
        await query.message.edit_text("Админы:\n- Лидер: @DektrianTV\n- Заместители: @Admin1 @Admin2", reply_markup=get_main_buttons())

# Основная функция запуска
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
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
            SCREENSHOT_1: [MessageHandler(filters.PHOTO | filters.TEXT, screenshot_1)],
            SCREENSHOT_2: [MessageHandler(filters.PHOTO | filters.TEXT, screenshot_2)],
        },
        fallbacks=[CallbackQueryHandler(button_callback)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))

    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://clan-bot-2-1.onrender.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
