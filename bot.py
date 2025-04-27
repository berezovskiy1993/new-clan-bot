from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import os

# Токен и ID администратора
TOKEN = '7912601677:AAE_saIpU_55S2dgEdnEnnXov0pw33BPVu0'
ADMIN_ID = 894031843  # ID администратора

# Состояния для ConversationHandler
NICKNAME, PLAYER_ID, AGE, KD, MATCHES, CONFIRMATION_NICKNAME, CONFIRMATION_PLAYER_ID, CONFIRMATION_AGE, CONFIRMATION_KD, CONFIRMATION_MATCHES = range(10)

# Стартовая функция
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Привет! Я бот клана DEKTRIAN FAMILY. Хочешь вступить в наш клан? Пожалуйста, отправь заявку!")
    return NICKNAME

# Получение никнейма
async def nickname(update: Update, context: CallbackContext) -> int:
    context.user_data['nickname'] = update.message.text
    await update.message.reply_text(f"Ваш никнейм: {context.user_data['nickname']}. Подтверждаете? (Да/Нет)")
    return CONFIRMATION_NICKNAME

# Подтверждение никнейма
async def confirmation_nickname(update: Update, context: CallbackContext) -> int:
    response = update.message.text.strip().lower()
    if response in ['да', 'yes']:
        await update.message.reply_text("Отлично! Теперь, пожалуйста, укажите свой игровой айди.")
        return PLAYER_ID
    elif response in ['нет', 'no']:
        await update.message.reply_text("Пожалуйста, введите ваш никнейм снова.")
        return NICKNAME
    else:
        await update.message.reply_text("Пожалуйста, ответьте 'Да' или 'Нет'.")
        return CONFIRMATION_NICKNAME

# Получение игрового ID
async def player_id(update: Update, context: CallbackContext) -> int:
    player_id = update.message.text
    if not player_id.isdigit():
        await update.message.reply_text("Айди должно состоять только из чисел. Пожалуйста, введите правильный айди.")
        return PLAYER_ID
    
    context.user_data['player_id'] = player_id
    await update.message.reply_text(f"Ваш игровой айди: {context.user_data['player_id']}. Подтверждаете? (Да/Нет)")
    return CONFIRMATION_PLAYER_ID

# Подтверждение игрового ID
async def confirmation_player_id(update: Update, context: CallbackContext) -> int:
    response = update.message.text.strip().lower()
    if response in ['да', 'yes']:
        await update.message.reply_text("Теперь укажите свой возраст.")
        return AGE
    elif response in ['нет', 'no']:
        await update.message.reply_text("Пожалуйста, введите ваш игровой айди снова.")
        return PLAYER_ID
    else:
        await update.message.reply_text("Пожалуйста, ответьте 'Да' или 'Нет'.")
        return CONFIRMATION_PLAYER_ID

# Получение возраста
async def age(update: Update, context: CallbackContext) -> int:
    age = update.message.text
    if not age.isdigit():
        await update.message.reply_text("Возраст должен быть числом. Пожалуйста, введите правильный возраст.")
        return AGE
    
    context.user_data['age'] = age
    await update.message.reply_text(f"Ваш возраст: {context.user_data['age']}. Подтверждаете? (Да/Нет)")
    return CONFIRMATION_AGE

# Подтверждение возраста
async def confirmation_age(update: Update, context: CallbackContext) -> int:
    response = update.message.text.strip().lower()
    if response in ['да', 'yes']:
        await update.message.reply_text("Какая у тебя КД за последние два сезона?")
        return KD
    elif response in ['нет', 'no']:
        await update.message.reply_text("Пожалуйста, введите свой возраст снова.")
        return AGE
    else:
        await update.message.reply_text("Пожалуйста, ответьте 'Да' или 'Нет'.")
        return CONFIRMATION_AGE

# Получение КД
async def kd(update: Update, context: CallbackContext) -> int:
    kd = update.message.text
    if not kd.isdigit():
        await update.message.reply_text("КД должно быть числом. Пожалуйста, введите правильное КД.")
        return KD
    
    context.user_data['kd'] = kd
    await update.message.reply_text(f"Ваш КД: {context.user_data['kd']}. Подтверждаете? (Да/Нет)")
    return CONFIRMATION_KD

# Подтверждение КД
async def confirmation_kd(update: Update, context: CallbackContext) -> int:
    response = update.message.text.strip().lower()
    if response in ['да', 'yes']:
        await update.message.reply_text("Сколько матчей ты сыграл в этом и прошлом сезоне?")
        return MATCHES
    elif response in ['нет', 'no']:
        await update.message.reply_text("Пожалуйста, введите свой КД снова.")
        return KD
    else:
        await update.message.reply_text("Пожалуйста, ответьте 'Да' или 'Нет'.")
        return CONFIRMATION_KD

# Получение матчей
async def matches(update: Update, context: CallbackContext) -> int:
    matches = update.message.text
    if not matches.isdigit():
        await update.message.reply_text("Количество матчей должно быть числом. Пожалуйста, введите правильное количество матчей.")
        return MATCHES
    
    context.user_data['matches'] = matches
