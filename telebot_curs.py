import telebot
import extensions as ex
from resources.token_and_keys import TOKEN
from resources.message_for_user import START_HELP, VALUES

# Хотел бы узнать можно ли писать так, как написан ниже bot.
bot = telebot.TeleBot(TOKEN)


def main():
    @bot.message_handler(commands=["start", "help"])
    def start_message(message: telebot.types.Message):
        bot.send_message(message.chat.id, START_HELP)

    @bot.message_handler(commands=["values"])
    def message_handler_values_help(message: telebot.types.Message):
        bot.reply_to(message, "Пожалуйста, подождите 1 минуту.")
        bot.send_message(message.chat.id, f"{ex.ApiHandler.get_values()}{VALUES}")

    @bot.message_handler(content_types=["text"])
    def message_handler_values(message: telebot.types.Message):
        values = message.text.split()

        if len(values) > 3:
            raise ex.APIException(
                "ValueError: Введён неверный формат сообщения.\nНапишите /help, если требуеться помощь.",
                message.chat.id)

        if values[0] == values[1]:
            raise ex.APIException(
                "ValueError: Введёны две одинаковые валюты.\nНапишите /help, если требуеться помощь"
                " или /values, чтобы узнать список валют.",
                message.chat.id)
        try:
            int(values[2])
        except ValueError:
            raise ex.APIException(
                "ValueError: Не введено количество первой валюты.\nНапишите /help, если требуеться помощь.",
                message.chat.id)

        base, quote, amount = values

        # Перевод USD, EUR в RUB выдает старые катировки, но RUB в USD, EUR выдает актуальные катировки
        # Не знаю, как это можно исправить, но предполагаю, что нужно сменить API.
        bot.send_message(message.chat.id,
                         f"{base}: {amount}, {quote}:"
                         f" {ex.ApiHandler.get_price(base, quote, amount, message.chat.id)}")

    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
