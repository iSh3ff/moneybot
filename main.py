import telebot

bot = telebot.TeleBot("5537548379:AAEBqWu9PleSUucg7V2NDiuTP2q-NTGFL1I")

from config import keys, TOKEN
from extensions import get_amount, get_currency,ConvertionException, CurrencyConverter

@bot.message_handler (commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветсвую!\n Я Бот который умеет конвертировать валюту!\nПример сообщения:\n"10 юаней в рубли"\n\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler (commands=['values'])
def values(message: telebot.types.Message):
    text = 'Валюты доступные для перевода:'
    for key in keys.keys():
        text = '\n- '.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler (content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = message.text.split()
        total_base = CurrencyConverter.convert(text)
    except ConvertionException as e:
        bot.reply_to(message, f'Не удалось обработать запрос 🤓 \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду со стороны программы!\n{e}')
    else:
        text_2 = f'Цена {get_amount(text)} {keys[get_currency(text)[0]]} в {keys[get_currency(text)[-1]]} - {total_base * get_amount(text)}'
        bot.send_message(message.chat.id, text_2)

bot.polling(none_stop=True)
