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
import time, os, random, socks, requests
import multiprocessing
from multiprocessing import Pool
from seleniumwire import webdriver
from selenium.webdriver import *

# pyinstaller --onedir -D WEB.py
# pyinstaller --onefile main.py

############################    S E T T I N G S    ############################
LOCAL_DIR = os.getcwd()

START_PORT = 8001
END_PORT = 9050

def open_proxy():
    print("Проверяем прокси перед работой... Это может занять некоторое время.")
    PROXY_BASE = []
    with open(f'{LOCAL_DIR}\\proxy\\http.txt', 'r', encoding='utf-8') as file:
        all_file = file.read()
    
    for line in all_file.split("\n"):
        if ":" in line:
            data = line.split(":")
            test_proxy = f'http://{data[2]}:{data[3]}@{data[0]}:{data[1]}'
            try:
                requests.get('http://httpbin.org/ip',proxies=dict(http=test_proxy,https=test_proxy))
                PROXY_BASE.append(f'{data[2]}:{data[3]}@{data[0]}:{data[1]}')
            except:
                pass

    print(f"Найдено {len(PROXY_BASE)} рабочих прокси. ")
    return PROXY_BASE

############################   C  L  A  S  S   ############################
class Web():

    def __init__(self,headles=False,url='https://t.me/s/testlinkformyproject/',agent ="0",tor_proxy="1",scroll="0"):
        if "t.me/s/" not in url and "t.me/" in url:
            self.url = "https://t.me/s/" + url.split("t.me/")[1]
        else:
            self.url = url
        self.headles = headles
        self.agent = agent
        self.tor_proxy = tor_proxy
        self.scroll = scroll
        self.mobile_agents = []
        self.user_agents = []

        with open(f'{LOCAL_DIR}\\agents.txt', 'r', encoding='utf-8') as file:
            data = file.read()

        for line in data.split("\n") :
            if "Mobile" in line :
                self.mobile_agents.append(line)
            else:
                self.user_agents.append(line)

        self.all_agents = self.mobile_agents + self.user_agents

    def random_agent(self):
        if self.agent == "0":
            return random.choice(self.all_agents)
        elif self.agent == "1":
            return random.choice(self.mobile_agents)
        else:
            return random.choice(self.user_agents)

    def seleniumwire_options(self,port):
        if self.tor_proxy == "1":
            return {
                'proxy': {
                        'http': f'socks5://localhost:{port}',
                        'https': f'socks5://localhost:{port}',
                        'no_proxy': f'socks5://localhost:{port}'
                        }
            }
        else:
            
            return {
                'proxy': {
                        'http': f'http://{port}',
                        'https': f'https://{port}'
                        }
            }

    def browser_option(self):
        option = FirefoxOptions()
        option.set_preference("general.useragent.override", self.random_agent()) # Меняем юзерагент
        option.set_preference('dom.webdriver.enabled',False) # Пытаемся скрыть силениум
        option.set_preference('dom.webnotifications.enabled',False) # Пытаемся скрыть силениум
        option.set_preference('useAutomationExtension', False) # Пытаемся скрыть силениум
        option.set_preference('navigator.webdriver', "undefined") # Пытаемся скрыть силениум
        option.set_preference("javascript.enabled", True)
        option.set_preference('media.volume_scale','0.0') # Выключим звук
        option.set_preference("--disable-infobars",True)
        option.set_preference("--disable-notifications",True)
        option.set_preference('--disable-gpu',True)
        option.headless = self.headles
        return option

    def selenium_work(self,port):
        fl_sleep = False
        try:
            time.sleep(random.randint(10,100)/100)
            driver = webdriver.Firefox(options=self.browser_option(),
                                    executable_path=f'{LOCAL_DIR}\\driver\\geckodriver.exe',
                                    seleniumwire_options=self.seleniumwire_options(port))
            print(f"Сконфигурили браузер. Порт\Прокси {port}")

            driver.get(self.url)
            time.sleep(random.randint(10,200)/100)
            if (self.scroll == "0" and random.choice([True,False])) or self.scroll == "1":
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Успешно просмотрели пост. Порт\Прокси {port}")
        except Exception as e:
            print('Ошибка : ' + str(e))
            fl_sleep = True
        finally:  
            try:
                driver.close()
                driver.quit()
            except:
                pass
            if fl_sleep:
                time.sleep(random.randint(20,60))
            

############################   W  O  R  K   ############################
def main():
    url = input("Введите адрес группы для накрутки:\n") 
    agent = input("Укажите тип просмотра 0 - Случайно  1 - Мобильные  2 - Десктопные:\n")
    process_count = int(input("Укажите количество параллельных процессов (Максимум 20):\n"))
    tor_proxy = input("Укажите тип прокси 0 - Папка proxy,  1 - Тор:\n")
    scroll = input("Укажите 0 - случайная прокрутка, 1 - принудительная прокрутка, 2 - без прокрутки :\n")

    if tor_proxy == '1':
        work_base = list(range(8001,9050))
    else:
        work_base = open_proxy()

    web_obj = Web(headles = True,url = url,agent = agent,tor_proxy=tor_proxy, scroll=scroll)
    p = Pool(processes=process_count)
    p.map(web_obj.selenium_work, work_base)



if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("#####     Н А К Р У Т К А   П Р О С М О Т Р О В   W E B     #####")
    main()
    input("Нажмите Enter для завершения работы...")