import telebot
import requests
from dadata import Dadata


class StartBot:
    with open("resourses/token.txt", "r") as f:
        bot = telebot.TeleBot(f.read().strip())
    dadata = Dadata("bd2b741530239b914d747ea758e4fbdbabf6a413")


class Reform:
    @staticmethod
    def reform_to_str(response):
        values = []
        values_str = ""
        for texts in response:
            for text in texts["symbol"].split("/"):
                if text not in values:
                    values.append(text)
                    data = StartBot.dadata.find_by_id("currency", text)
                    if data:
                        name = data[0]["data"]["name"]
                        values_str += f"{text} - {name}\n"
                    else:
                        values_str += f"{text} - Не найдено в базе\n"
        return values_str


class ApiHandler:
    @staticmethod
    def get_price(base, quote, amount):
        response = requests.get(
            f"https://fcsapi.com/api-v3/forex/latest?symbol={base}/{quote}&access_key=VLMJJVX52PxyQgAuN0FX8xcz").json()
        return str(float(amount) * float(response["response"][0]["c"]))

    @staticmethod
    def get_values():
        response = requests.get(
            "https://fcsapi.com/api-v3/forex/list?type=forex&access_key=VLMJJVX52PxyQgAuN0FX8xcz").json()
        return Reform.reform_to_str(response["response"])


class TelegramBot:
    @staticmethod
    @StartBot.bot.message_handler(commands=["start", "help"])
    def start_message(message: telebot.types.Message):
        StartBot.bot.send_message(message.chat.id, "Приветствую!\nДля того, чтобы использовать этого бота, "
                                                   "нужно написать одним сообщением:\n"
                                                   "1) Имя валюты, цену которую нужно узнать.\n"
                                                   "2) Имя валюты, в которой надо узнать цену первой валюты.\n"
                                                   "3) Количество первой валюты.\n"
                                                   "Пример сообщения: USD RUB 100.\n"
                                                   "Чтобы узнать, какие валюты есть в списке бота пропешите /values.\n"
                                                   "Напишите /help если понадобиться помощь.")

    @staticmethod
    @StartBot.bot.message_handler(commands=["values"])
    def message_handler_values_help(message: telebot.types.Message):
        StartBot.bot.reply_to(message, "Пожалуйста, подождите 1 минуту.")
        StartBot.bot.send_message(message.chat.id,
                                  f"{ApiHandler.get_values()}"
                                  f"\nВнимание! Некоторые из валют невозможно перевести в другие,"
                                  f" но большая часть списка переводяться в Евро и Доллары!")

    @staticmethod
    @StartBot.bot.message_handler(content_types=["text"])
    def message_handler_values(message: telebot.types.Message):
        base, quote, amount = map(str, message.text.split())
        StartBot.bot.send_message(message.chat.id,
                                  f"{base}: {amount}, {quote}: {ApiHandler.get_price(base, quote, amount)}")
