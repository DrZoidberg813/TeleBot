import telebot


def main():
    bot = telebot.TeleBot("5467825236:AAGwd8YyjxwdIhG0LVHNy2YJJ6lozdnZZuk")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
