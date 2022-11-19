from telebot_curs import bot
import requests
from dadata import Dadata
from resources.token_and_keys import KEY, KEY_DADATA

# Хотел бы узнать можно ли писать так, как написан ниже dadata.
dadata = Dadata(KEY_DADATA)


class APIException(Exception):
    def __init__(self, message_er, chat_id):
        super(APIException, self).__init__(message_er)
        bot.send_message(chat_id, message_er)


class Reform:
    @staticmethod
    def reform_to_str(response):
        values = []
        values_str = ""
        for texts in response:
            for text in texts["symbol"].split("/"):
                if text not in values:
                    values.append(text)
                    data = dadata.find_by_id("currency", text)
                    if data:
                        name = data[0]["data"]["name"]
                        values_str += f"{text} - {name}\n"
                    else:
                        values_str += f"{text} - Название не найдено в базе\n"
        return values_str


class ApiHandler:
    @staticmethod
    def get_price(base, quote, amount, message_chat_id):
        try:
            response = requests.get(
                f"https://fcsapi.com/api-v3/forex/latest?symbol={base}/{quote}&access_key={KEY}").json()
            return str(float(amount) * float(response["response"][0]["c"]))
        except KeyError:

            # Здесь идет вывод ошибки из-за того, что в базе API есть около 2000 возможных конвертаций
            # но не все валюты можно конвертировать друг в друга, а выводить 2000 конвертаций слишком громоздко
            raise APIException("KeyError: Валюты нет в базе данных или невозможна конвертация валют.\n"
                               "Чтобы узнать, какие валюты есть в списке бота напишите /values.",
                               message_chat_id)

    @staticmethod
    def get_values():
        response = requests.get(
            f"https://fcsapi.com/api-v3/forex/list?type=forex&access_key={KEY}").json()
        return Reform.reform_to_str(response["response"])
