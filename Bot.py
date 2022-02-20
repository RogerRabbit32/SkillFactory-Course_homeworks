import telebot
from Config import TOKEN, currencies
from Extensions import CurrencyConverter, MyBotException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Для конвертации введите: \n' \
           '<из чего переводим> <во что переводим> <сколько>' \
           '\n \n' \
           'Например: USD RUB 600 \n \n' \
           'Посмотреть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for currency in currencies.keys():
        text = '\n'.join((text, f'{currency} {currencies[currency]}'))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise MyBotException('Введите две валюты и сумму')

        quote, base, amount = values
        conv_result = CurrencyConverter.convert(quote, base, amount)

    except MyBotException as e:
        bot.reply_to(message, f'Ошибка. {e}')
    except Exception:
        bot.reply_to(message, f'Что-то сломалось. Просим прощения :(.')
    else:
        text = f'Стоимость {amount} {quote} в {base}: {conv_result}'
        bot.send_message(message.chat.id, text)


bot.polling()
