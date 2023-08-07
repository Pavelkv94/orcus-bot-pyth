from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


#start
def start(bot, message):

    welcome_text = (
        "Привет! 👋 \n\n"
        "Добро пожаловать в бота, специализирующегося на хакинге, инфобезопасности и взломе информационных систем. \n\n"
        "🔒 Здесь вы можете изучить методы атак и защиты, разбираться в шифровании и анализе уязвимостей. "
        "Я не поощряю противозаконные действия или противоправные действия в сети. "
        "Моя цель — помочь развивать твои знания в области информационной безопасности и осознанное использование полученной информации.\n\n"
        "🔐 Не забывай, что хакинг и взлом без разрешения владельца системы — противозаконные действия. "
        "Важно соблюдать этический кодекс и использовать полученные знания в законных целях. "
        "Обращайся со своими вопросами, будем исследовать мир информационной безопасности вместе! 💻🛡️"
    )

    with open('./assets/welcome.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file, caption=welcome_text)

#menu
def show_menu(bot, chat_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    show_tools_button = InlineKeyboardButton(
        text="🛠 Показать инструменты 🛠", callback_data="show_tools")
    keyboard.add(show_tools_button)

    message_options = {
        "reply_markup": keyboard,
    }

    bot.send_message(chat_id, "Выберите опцию:", **message_options)