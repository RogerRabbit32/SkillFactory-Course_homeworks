import requests
import json
from Config import currencies


class MyBotException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise MyBotException(f'Не имеет смысла переводить {quote} в {quote}.')
        quote, base = quote.lower(), base.lower()

        try:
            quote_symbol = currencies[quote]
        except KeyError:
            raise MyBotException(f'В боте нет такой валюты как {quote}.')
        try:
            base_symbol = currencies[base]
        except KeyError:
            raise MyBotException(f'В боте нет такой валюты как {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise MyBotException('Сумма должна быть числом.')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={quote_symbol}_{base_symbol}&compact=ultra&apiKey=35dd6c11227e9eb6094a')
        interim_text = json.loads(r.content)[f'{currencies[quote]}_{currencies[base]}']
        conv_result = round(interim_text * float(amount), 2)
        return conv_result
