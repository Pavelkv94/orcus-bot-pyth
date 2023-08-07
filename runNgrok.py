import subprocess

def run_ngrok(chat_id, bot):
    try:
        # Run ngrok using subprocess
        ngrok_process = subprocess.Popen(["ngrok", "http", "4001"])
        ngrok_process.wait()  # Wait for ngrok to start
        
        # Get the ngrok HTTP address from the output
        ngrok_output = ngrok_process.communicate()[0].decode()
        http_address = ngrok_output.split('\n')[2].split(' ')[1]
        
        bot.send_message(chat_id, f"Ngrok HTTP address: {http_address}")
        
    except Exception as e:
         bot.send_message(chat_id, f"An error occurred: {str(e)}")
