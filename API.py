# не забыть obfs4proxy.exe
########################  torrc  ########################
# DataDirectory C:\Tor
# GeoIPFile C:\Tor\geoip
# GeoIPv6File C:Tor\geoip6
# AvoidDiskWrites 1
# ClientTransportPlugin obfs4 exec C:\Tor\obfs4proxy.exe
# Bridge obfs4 185.177.207.186:8443 E8C2C83BA333B5C4F6A5FC4798C62BA6B7CCF60E cert=6yRznmuljBhZ+Afu7zOBoVVz9Ho6LnB3z3OaiYFiBQLew5m5EVXeq6+fxKH0zZ0Rf3F6RA iat-mode=0
# Bridge obfs4 89.58.12.52:3487 48A2BD4E1A942A3F4A73B4F5EE8D078725903411 cert=d9SvwoZdikmTz7v6w3MkqCxt9TDCe94TaNNz4950m9terWW1h+Y6IwdGF4jaS1cmasU3Wg iat-mode=0
# Bridge obfs4 46.226.106.27:9134 D7038AC390D88633F7B69C0A231B5C422B9AECE3 cert=ZckPin/938VBzulmflvy2eMdfN/N5e6ZctCbSxcvoOgX1fWoeA+hTiiqcZdinj/SfZXKEw iat-mode=0
# UseBridges 1

# ControlPort 9051
# HashedControlPassword 16:6D57544BEC2B1F0360C80026913D5A175F3D6E16FE04104F65749F7468
# CookieAuthentication 1

# SOCKSPort 9050 


# HeartbeatPeriod 1 hours
# ExitRelay 0

# ExcludeExitNodes {ru},{ua},{by},{kz},{??}
# StrictNodes 1
##########################################################
import requests, os, json, socks, random, time
import multiprocessing
from multiprocessing import Pool

from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest,GetMessagesViewsRequest
from telethon.tl.functions.channels import JoinChannelRequest

# pyinstaller --onedir -D API.py

############################    S E T T I N G S    ############################
LOCAL_DIR = os.getcwd()

START_PORT = 8001
END_PORT = 9050

def jsone_session(ID,dir="data_api"):
    with open(f'{LOCAL_DIR}\\{dir}\\{ID}.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    json_out = {'session_file':False,
                'app_id':None,
                'app_hash':None,
                'first_name':None,
                'last_name':None,
                'sdk':"Android 7.0 Nougat",
                'app_version':"PS(22)",
                'device':"Huawei P Smart S Midnight Black",
                'lang_pack':"android",
                'proxy':None,
                'ipv6':False,
                'password_str':None}

    for key in list(json_out) + ['my_2fa','twoFA']:
        try:
            json_out[key] = json_data[key]
        except:
            pass
        
    return json_out

def session_base(dir="data_api"):
    base = []
    for file_name in os.listdir(f'{LOCAL_DIR}\\{dir}'):
        if ".session" in file_name and "journal" not in file_name:
            base.append(file_name.split(".session")[0])
    return base

def test_ip(port = 9050):
    url = 'http://httpbin.org/ip'
    res = requests.get(url,proxies={'http':f'socks5://localhost:{port}', 
                                    'https':f'socks5://localhost:{port}'})
    IP = res.text.split(":")[1].split("\n")[0]
    print(f"Получили IP : {IP}")

def open_proxy():
    fl_good = False
    with open(f'{LOCAL_DIR}\\proxy\\socks5.txt', 'r', encoding='utf-8') as file:
        all_file = file.read()
    while not fl_good:
        line = random.choice(all_file.split("\n"))
        data = line.split(":")
        proxy = (socks.SOCKS5,data[0],int(data[1]),data[2],data[3])
        test_proxy = f'socks5://{data[2]}:{data[3]}@{data[0]}:{data[1]}'
        try:
            requests.get('http://httpbin.org/ip',proxies=dict(http=test_proxy,https=test_proxy))
            fl_good = True
        except:
            pass

    return proxy

############################   C  L  A  S  S   ############################
class API():
    def __init__(self,url,view_count=100,join_flag="1",tor_flag="1"):
        self.url = url
        self.view_count = view_count
        self.join_flag = join_flag
        self.tor_flag = tor_flag

    def _remove_session(self,ID,dir):
        for postfix in [".json",".session-journal",".session"]:
            try:
                os.remove(f"{LOCAL_DIR}\\{dir}\\{ID}{postfix}")
            except:
                pass

    def _client(self,ID = random.choice(session_base()),dir="data_api"):
        def _bad_client(client,ID):
            try:
                client.disconnect()
            except:
                pass
            self._remove_session(ID,dir)
        session_data = jsone_session(ID,dir)
        if self.tor_flag =="1":
            port = random.randint(START_PORT,END_PORT)
            proxy=(socks.SOCKS5, '127.0.0.1', port)
        else:
            proxy = open_proxy()
        client = TelegramClient(session=f'{LOCAL_DIR}\\{dir}\\{ID}',
                                    api_id=session_data['app_id'],
                                    api_hash=session_data['app_hash'],
                                    use_ipv6=session_data['ipv6'],
                                    proxy=proxy,
                                    device_model=session_data['device'],
                                    system_version=session_data['sdk'],
                                    app_version=session_data['app_version']
                                    )
        client.connect()
        if client.is_user_authorized():
            return client
        else:
            _bad_client(client,ID)
            return False

    def view_message(self,ID):
        try:
            print(f"API | Сессия {ID} | Запустили процесс просмотра.")
            with self._client(ID) as client:
                chanal_input_entity = client.get_input_entity(self.url)
                if self.join_flag == 1:
                    try:
                        client(JoinChannelRequest(channel=chanal_input_entity))
                    except Exception as e:
                        pass
                history = client(GetHistoryRequest(peer=chanal_input_entity, 
                                                offset_id=0, 
                                                offset_date=None, 
                                                add_offset=0,
                                                limit=self.view_count, 
                                                max_id=0, 
                                                min_id=0, 
                                                hash=0))

                id_base = []
                for message in history.messages:
                    id_base.append(int(message.id))
 
                client(GetMessagesViewsRequest(
                    peer=chanal_input_entity,
                    id=id_base,
                    increment=True
                    ))
                
            print(f"API | Сессия {ID} | Успешно просмотрели сообщения.")
        except Exception as e:
            print(f"API | Сессия {ID} | Ошибка : {str(e)}.")

def main():
    url = input("Введите адрес группы для накрутки:\n")
    session_count = int(input(f"Введите количество параллельных сессий (максимум {len(session_base())}):\n"))
    view_count = int(input(f"Введите количество просматриваемых сообщений:\n"))
    join_flag = int(input(f"Введите 0 - без подписки, 1 - с подпиской на канал:\n"))
    tor_flag = int(input(f"Введите 0 - для работы через прокси, 1 - через ТОР:\n"))
    api_pool = Pool(processes=session_count)
    api_pool.map(API(url,view_count,join_flag,tor_flag).view_message, session_base())
    api_pool.close()
    api_pool.join()
    print("API | Процессы | Завершили все активные процессы.")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("#####     Н А К Р У Т К А   П Р О С М О Т Р О В   A P I     #####")
    main()
    input("Нажмите Enter для завершения работы...")
