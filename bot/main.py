from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import requests
import os
from datetime import datetime

item_list = []

def get_price(item):
    url = f'http://127.0.0.1:5000/api/{item}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Ошибка получения данных'

def get_items():
    url = f'http://127.0.0.1:5000/api/items'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Функция для получения списка валют и отправки их в чат
def get_currency_list(update: Update, context: CallbackContext) -> None:
    currency_list = get_items()
    if currency_list:
        message_text = f"Доступные виды валют: {', '.join(currency_list)}"
    else:
        message_text = "Извините, список валют временно недоступен."
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Выбрать другой курс", callback_data='restart')]
    ])
    context.bot.send_message(chat_id=update.message.chat_id, text=message_text, reply_markup=reply_markup)

# Обработчик для команды /get_rate
def get_rate(update: Update, context: CallbackContext) -> None:
    # Проверяем, что это первое сообщение после команды
    if context.args:
        currency_code = context.args[0].lower()
    elif update.message.text:
        currency_code = update.message.text.lower()
    else:
        update.message.reply_text('Пожалуйста, введите код валюты после команды, например, USD')
        return

    # Проверяем, что введенный код валюты находится в списке доступных
    if currency_code not in item_list:
        update.message.reply_text(f"Введите доступную валюту из списка: {', '.join(item_list)}")
        return

    # Получаем цену и текущую дату и время
    price = get_price(currency_code)
    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    if price != 'Ошибка получения данных':
        message_text = f"На момент {current_datetime} курс {currency_code} к рублю составляет:\n1 {currency_code} = {price} рублей"
    else:
        message_text = "Извините, данные временно недоступны."
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Выбрать другой курс", callback_data='restart')]
    ])
    context.bot.send_message(chat_id=update.message.chat_id, text=message_text, reply_markup=reply_markup)

# Обработчик для введенных сообщений (не команд)
def handle_messages(update: Update, context: CallbackContext) -> None:
    # Проверяем, что сообщение не является командой
    if not update.message.text.startswith('/'):
        get_rate(update, context)

# Функция обработки команды старт
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я ТаМарКа!\nИ я хочу помочь вам с вашим вопросом. Выберите раздел или введите требуемую валюту.')
    button_message(update=update, context=context)

def button_message(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Курсы валют", callback_data='currency')],
        [InlineKeyboardButton("Курсы металлов", callback_data='metals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Какой курс вы хотите узнать?", reply_markup=reply_markup)

# Функция обработки кнопок
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category = query.data
    keyboard = []

    if category == 'currency':
        keyboard = [
            [InlineKeyboardButton("Курс юаня", callback_data='currency_cnyrub')],
            [InlineKeyboardButton("Курс доллара", callback_data='currency_dollarrub')]
        ]
    elif category == 'metals':
        keyboard = [
            [InlineKeyboardButton("Курс стали", callback_data='metals_steel')],
            [InlineKeyboardButton("Курс чугуна", callback_data='metals_iron')]
        ]

    # Добавляем кнопку для повторного выбора
    keyboard.append([InlineKeyboardButton("Выбрать другой курс", callback_data='restart')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите интересующую вас опцию:", reply_markup=reply_markup)

# Функция для отображения цены
def show_price(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    _, item = query.data.split("_")
    price = get_price(item)

    # Получаем текущую дату и время
    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    if price != 'Нет данных':
        message_text = f"На момент {current_datetime} курс {item} к рублю составляет:\n1 {item} = {price} у.е."
    else:
        message_text = "Извините, данные временно недоступны."

    # Отправляем результат в новом сообщении с кнопкой для повторного выбора
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Выбрать другой курс", callback_data='restart')]
    ])
    context.bot.send_message(chat_id=query.message.chat_id, text=message_text, reply_markup=reply_markup)

# Функция для обработки повторного выбора
def restart(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Отправляем приветственное сообщение снова
    button_message(update=update, context=context)

# Основной блок
def main():
    
    #bot_token = os.getenv("BOT_TOKEN")
    TOKEN = '6449226644:AAEXsQkSGSjBs8tAlRYyDSgkO5C_8zdVcBo'
    
    global item_list 
    item_list = get_items()

    updater = Updater(TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern='^(currency|metals)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_price, pattern='^(currency_|metals_)'))
    dispatcher.add_handler(CallbackQueryHandler(restart, pattern='^restart$'))
    dispatcher.add_handler(CommandHandler('get_rate', get_rate, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))
    dispatcher.add_handler(CommandHandler('currencies', get_currency_list))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
