import requests


def get_ngrok_http_address(chat_id, bot):
    ngrok_api_url = "http://127.0.0.1:4040/api/tunnels"

    try:
        response = requests.get(ngrok_api_url)
        data = response.json()
        bot.send_message(
            chat_id, f'Используйте данный url для получения данных обьекта.\n\n {data["tunnels"][0]["public_url"]} \n\n 🔐 Не забывайте, что хакинг и взлом без разрешения владельца системы — противозаконные действия. Важно соблюдать этический кодекс и использовать полученные знания в законных целях. ')
        # return data["tunnels"][0]["public_url"]

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # return None

# # Example usage
# ngrok_http_address = get_ngrok_http_address()
# if ngrok_http_address:
#     print(f"Ngrok HTTP address: {ngrok_http_address}")
# else:
#     print("Failed to retrieve Ngrok HTTP address")
