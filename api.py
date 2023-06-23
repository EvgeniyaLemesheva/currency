import requests
import json

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}

class APIException(Exception):
    pass

BOT_TOKEN = "6040529044:AAEsvj1nXNOA9PoEc3Z5BwJePdsNq-2o2io"


class API:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"http://api.exchangeratesapi.io/latest?access_key=bee740e74b77c976c09aac0b7528d8ab&from={base}&to={quote}"
        response = requests.get(url)
        data = json.loads(response.text)

        if 'error' in data:
            raise APIException(f"Ошибка получения курса: {data['error']}")

        rate = data['rates'].get(quote)
        if rate is None:
            raise APIException(f"Ошибка получения курса: Валюта {quote} не найдена.")

        price = round(rate * amount, 2)
        return price
