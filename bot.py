from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES, CONFIRMATION = range(6)

# Стартовая функция с кнопкой
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [[InlineKeyboardButton("Начать заявку", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Хочешь вступить в наш клан? Пожалуйста, отправь заявку!", reply_markup=reply_markup)
    return NICKNAME

# Функция для начала заявки после нажатия кнопки
async def start_application(update: Update, context: CallbackContext) -> int:
    await update.callback_query.answer()
    await update.callback_query.message.edit_text("Отлично! Пожалуйста, укажи свой никнейм.")
    return NICKNAME

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data="next_player_id")],
        [InlineKeyboardButton("Отменить", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Теперь, пожалуйста, укажи свой игровой айди.", reply_markup=reply_markup)
    return PLAYER_ID

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("Айди должен состоять только из чисел. Пожалуйста, попробуй снова.")
        return PLAYER_ID
    
    context.user_data['player_id'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data="next_age")],
        [InlineKeyboardButton("Назад", callback_data="back_nickname")],
        [InlineKeyboardButton("Отменить", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Теперь укажи свой возраст.", reply_markup=reply_markup)
    return AGE

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("Возраст должен состоять только из чисел. Пожалуйста, попробуй снова.")
        return AGE
    
    context.user_data['age'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data="next_kd")],
        [InlineKeyboardButton("Назад", callback_data="back_player_id")],
        [InlineKeyboardButton("Отменить", callback
