import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import whois
# Replace with your bot token
TOKEN = "6618317228:AAHJENt4uNJ6h773Oow1RRdeNTehs8tg4qs"
bot = telebot.TeleBot(TOKEN)

# Dictionary to store conversation states
conversation_states = {}

@bot.message_handler(commands=['start'])
def start(message):

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


@bot.message_handler(commands=['menu'])
def menu(message):
    chat_id = message.chat.id  # Get the chat ID from the message object
    show_menu(chat_id)


def show_menu(chat_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    show_tools_button = InlineKeyboardButton(
        text="🛠 Показать инструменты 🛠", callback_data="show_tools")
    keyboard.add(show_tools_button)

    message_options = {
        "reply_markup": keyboard,
    }

    bot.send_message(chat_id, "Выберите опцию:", **message_options)


@bot.callback_query_handler(func=lambda query: True)
def handle_callback_query(query):
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if query.data == "show_tools":
        tools_text = "Выберите категорию:"

        keyboard = InlineKeyboardMarkup(row_width=1)
        sites_button = InlineKeyboardButton(
            text="Сайты", callback_data="sites")
        keyboard.add(sites_button)

        bot.edit_message_text(tools_text, chat_id=chat_id,
                              message_id=message_id, reply_markup=keyboard)

    elif query.data == "sites":
        tools_text = "Сайты"

        keyboard = InlineKeyboardMarkup(row_width=3)
        whois_button = InlineKeyboardButton(
            text="Whois", callback_data="whois")
        keyboard.add(whois_button)

        bot.edit_message_text(tools_text, chat_id=chat_id,
                              message_id=message_id, reply_markup=keyboard)

    elif query.data == "whois":
        # Set conversation state to "waiting_for_user_input"
        conversation_states[chat_id] = "waiting_for_user_input"

        whois_description = (
            "Whois - это утилита или сервис, который предоставляет информацию о регистрации доменных имен. "
            "Он позволяет получить данные о владельце домена, контактные данные, даты регистрации и другие сведения.\n\n"
            "Чтобы воспользоваться данным сервисом введите доменное имя без протокола либо его IP адрес:"
        )

        bot.send_message(chat_id=chat_id, text=whois_description)

@bot.message_handler(func=lambda message: conversation_states.get(message.chat.id) == "waiting_for_user_input")

def handle_user_input(message):
    chat_id = message.chat.id
    input_text = message.text.strip()

    domen_check = re.compile(r'[a-zA-Zа-яА-ЯёЁ0-9_-]+(\.[a-zA-Zа-яА-ЯёЁ0-9_-]+)*\.[a-zA-Zа-яА-ЯёЁ]{2,5}')
    ip_check = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]?)$')

    if domen_check.match(input_text) or ip_check.match(input_text):
        try:
            whois_info = whois.whois(input_text)


            if whois_info.status and isinstance(whois_info.status, list) and whois_info.status[0] == None:
                bot.send_message(chat_id, "No WHOIS data available for the input.")
            else:
                response = "✅ WHOIS data for {}:\n\n".format(input_text)
                for key, value in whois_info.items():
                    response += "{}: {}\n".format(key, value)
                
                bot.send_message(chat_id, response)
        
        except Exception as e:
            bot.send_message(chat_id, "An error occurred. Please try again.")
    else:
        bot.send_message(chat_id, "👹 Invalid domain or IP resource.")

    conversation_states[chat_id] = None




@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id, "Available commands:\n/start - Start the bot\n/help - Show this help message")


bot.polling()


# def send_response(response):
#         bot.send_message(chat_id=chat_id, text=response)

#     try:
#         whois_data = whois.whois(input_text)
#         if whois_data.status:
#             response = "Статус: {}\n".format(whois_data.status)
#         else:
#             response = "Статус: Не найден\n"
        
#         if whois_data.registrar:
#             response += "Регистратор: {}\n".format(whois_data.registrar)
        
#         if whois_data.creation_date:
#             response += "Дата создания: {}\n".format(whois_data.creation_date)
        
#         if whois_data.expiration_date:
#             response += "Дата истечения: {}\n".format(whois_data.expiration_date)
        
#         if whois_data.domain_name:
#             response += "Доменное имя: {}\n".format(whois_data.domain_name)
        
#         if whois_data.org:
#             response += "Организация: {}\n".format(whois_data.org)
        
#         # You can add more attributes based on the WHOIS data you want to display
        
#         send_response(response)
#     except Exception as e:
#         send_response("Произошла ошибка: {}".format(str(e)))