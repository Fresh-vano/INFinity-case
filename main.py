from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import resources

def get_price(category, item):
    if category == 'currency':
        if item == 'dollar':
            rate = resources.CurrencyMOEXResource('USD').load_resource()
            return f"{rate} RUB" if rate != 'Нет данных' else rate
        elif item == 'yuan':
            rate = resources.CurrencyMOEXResource('CNY').load_resource()
            return f"{rate} RUB" if rate != 'Нет данных' else rate
    elif category == 'metals':
        if item == 'steel':
            rate = resources.MetalsLMEResource(['Ferrous', 'LME-Steel-CFR-India-Platts']).load_resource()
        elif item == 'cartIron':
            rate = resources.MetalsLMEResource(['Non-ferrous', 'LME-Aluminium']).load_resource()
        return f"{rate} USD/ton" if rate != None else rate
    else:
        return 'Нет данных'

# Функция обработки команды старт
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Курсы валют", callback_data='currency')],
        [InlineKeyboardButton("Курсы металлов", callback_data='metals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите категорию:', reply_markup=reply_markup)

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
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите интересующую вас опцию:", reply_markup=reply_markup)

# Функция для отображения цены
def show_price(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category, item = query.data.split('_')
    price = get_price(category, item)
    query.edit_message_text(text=f"Текущая цена: {price}")

# Основной блок
def main():
    # Вставьте ваш токен, полученный от BotFather, здесь
    TOKEN = '6449226644:AAEXsQkSGSjBs8tAlRYyDSgkO5C_8zdVcBo'
    
    updater = Updater(TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern='^(currency|metals)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_price, pattern='^(currency_|metals_)'))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
