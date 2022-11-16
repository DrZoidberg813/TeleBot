import telebot
import requests

with open("token.txt", "r") as f:
    bot = telebot.TeleBot(f.readline())


class ApiHandler:
    @staticmethod
    def get_price(base, quote, amount):
        response = requests.get(
            f"https://fcsapi.com/api-v3/forex/latest?symbol={base}/{quote}&access_key=VLMJJVX52PxyQgAuN0FX8xcz").json()
        return float(amount) * float(response["response"][0]["c"])


class TelegramBot:
    @staticmethod
    @bot.message_handler(commands=["start", "help"])
    def start_message(message: telebot.types.Message):
        bot.send_message(message.chat.id, "Приветствую!\nДля того, чтобы использовать этого бота, "
                                          "нужно написать одним сообщением:\n"
                                          "1) имя валюты, цену которую нужно узнать,\n"
                                          "2) имя валюты, в которой надо узнать цену первой валюты,\n"
                                          "3) количество первой валюты.\n"
                                          "Пример сообщения: USD RUB 100.")

    @staticmethod
    @bot.message_handler(content_types=["text"])
    def message_handler_values(message: telebot.types.Message):
        base, quote, amount = map(str, message.text.split())
        bot.send_message(message.chat.id, ex.ApiHandler.get_price(base, quote, amount))
