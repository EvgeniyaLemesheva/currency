import telebot
from api import API, APIException, BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Добро пожаловать!\n\n" \
                   "Этот бот возвращает цену на определенное количество валюты (евро, доллар или рубль).\n\n" \
                   "Чтобы узнать цену, отправьте сообщение в следующем формате:\n" \
                   "<имя валюты цену которой вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> " \
                   "<количество первой валюты>\n\n" \
                   "Например:\n" \
                   "USD RUB 100\n\n" \
                   "Для получения списка доступных валют введите команду /values."
    bot.send_message(message.chat.id, instructions)


@bot.message_handler(commands=['values'])
def send_currency_values(message):
    currency_values = "Доступные валюты:\n" \
                      "- Евро (EUR)\n" \
                      "- Доллар (USD)\n" \
                      "- Рубль (RUB)"
    bot.send_message(message.chat.id, currency_values)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text.strip().split(' ')
        if len(text) != 3:
            raise APIException("Неверный формат запроса. Проверьте инструкции с помощью команды /help.")

        base_currency, quote_currency, amount = text
        price = API.get_price(base_currency.upper(), quote_currency.upper(), float(amount))
        result = f"Цена {amount} {base_currency.upper()} в {quote_currency.upper()}: {price}"
        bot.send_message(message.chat.id, result)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка API: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
