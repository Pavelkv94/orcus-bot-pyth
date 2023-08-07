import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import whois
from commonOptions import start  # Import the start function
from commonOptions import show_menu  # Import the show_menu function
from handle_whois import handle_whois  # Import the show_menu function


# Replace with your bot token
TOKEN = "6618317228:AAHJENt4uNJ6h773Oow1RRdeNTehs8tg4qs"
bot = telebot.TeleBot(TOKEN)

# Dictionary to store conversation states
conversation_states = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    start(bot, message)

@bot.message_handler(commands=['menu'])
def menu(message):
    chat_id = message.chat.id  # Get the chat ID from the message object
    show_menu(bot, chat_id)




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

        keyboard = InlineKeyboardMarkup(row_width=1)
        whois_button = InlineKeyboardButton(
            text="Whois", callback_data="whois")
        seeker_button = InlineKeyboardButton(
            text="Seeker", callback_data="seeker")
        keyboard.add(whois_button)
        keyboard.add(seeker_button)

        bot.edit_message_text(tools_text, chat_id=chat_id,
                              message_id=message_id, reply_markup=keyboard)

    elif query.data == "whois":
        # Set conversation state to "waiting_for_user_input"
        if chat_id not in conversation_states:
            conversation_states[chat_id] = {}

        conversation_states[chat_id]["whois_input"] = "waiting_for_user_input"
        print(conversation_states)
        whois_description = (
            "Whois - это утилита или сервис, который предоставляет информацию о регистрации доменных имен. "
            "Он позволяет получить данные о владельце домена, контактные данные, даты регистрации и другие сведения.\n\n"
            "Чтобы воспользоваться данным сервисом введите доменное имя без протокола либо его IP адрес:"
        )

        bot.send_message(chat_id=chat_id, text=whois_description)

    elif query.data == "seeker":
        if chat_id not in conversation_states:
            conversation_states[chat_id] = {}

        # Set conversation state to "waiting_for_user_input"
        # conversation_states[chat_id] = "waiting_for_user_input"
        conversation_states[chat_id]["seeker_input"] = "waiting_for_user_input"
        print(conversation_states)

        # whois_description = (
        #     "Whois - это утилита или сервис, который предоставляет информацию о регистрации доменных имен. "
        #     "Он позволяет получить данные о владельце домена, контактные данные, даты регистрации и другие сведения.\n\n"
        #     "Чтобы воспользоваться данным сервисом введите доменное имя без протокола либо его IP адрес:"
        # )

        # bot.send_message(chat_id=chat_id, text=whois_description)



@bot.message_handler(func=lambda message: conversation_states.get(message.chat.id, {}).get("whois_input") == "waiting_for_user_input")

def handle_user_input(message):
    handle_whois(bot, message, conversation_states)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id, "Available commands:\n/start - Start the bot\n/help - Show this help message")


bot.polling()