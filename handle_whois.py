import re
import whois

def handle_whois(bot, message, conversation_states):
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

    conversation_states[chat_id]["whois_input"] = None