from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import resources
from datetime import datetime

def get_price(category, item):
    rate = None
    if category == 'currency':
        if item == 'dollar':
            rate = resources.CurrencyMOEXResource(['USD']).load_resource()
            return f"{rate} RUB" if rate != 'Нет данных' else rate
        elif item == 'yuan':
            rate = resources.CurrencyMOEXResource(['CNY']).load_resource()
            return f"{rate} RUB" if rate != 'Нет данных' else rate
    elif category == 'metals':
        if item == 'steel':
            rate = resources.MetalsRuInvestingResource(['us-steel-coil']).load_resource()
        elif item == 'castIron':
            rate = resources.MetalsRuInvestingResource(['iron-ore-62-cfr']).load_resource()
        return f"{rate} USD/ton" if rate != None else 'Нет данных'
    else:
        return 'Нет данных'

# Функция обработки команды старт
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я ТаМарКа!\nИ я хочу помочь вам с вашим вопросом.')
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
            [InlineKeyboardButton("Курс юаня", callback_data='currency_yuan')],
            [InlineKeyboardButton("Курс доллара", callback_data='currency_dollar')]
        ]
    elif category == 'metals':
        keyboard = [
            [InlineKeyboardButton("Курс стали", callback_data='metals_steel')],
            [InlineKeyboardButton("Курс чугуна", callback_data='metals_castIron')]
        ]

    # Добавляем кнопку для повторного выбора
    keyboard.append([InlineKeyboardButton("Выбрать другой курс", callback_data='restart')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите интересующую вас опцию:", reply_markup=reply_markup)

# Функция для отображения цены
def show_price(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category, item = query.data.split('_')
    price = get_price(category, item)

    # Получаем текущую дату и время
    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    if price != 'Нет данных':
        message_text = f"На момент {current_datetime} курс {item} к рублю составляет:\n1 {item} = {price} рублей"
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
    # Вставьте ваш токен, полученный от BotFather, здесь
    TOKEN = '6449226644:AAEXsQkSGSjBs8tAlRYyDSgkO5C_8zdVcBo'
    
    updater = Updater(TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern='^(currency|metals)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_price, pattern='^(currency_|metals_)'))
    dispatcher.add_handler(CallbackQueryHandler(restart, pattern='^restart$'))
    #dispatcher.add_handler(CallbackQueryHandler(button_message, pattern=''))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
