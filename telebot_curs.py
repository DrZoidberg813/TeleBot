from extensions import StartBot


def main():
    StartBot.bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
