import os, time, random
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver import *
# from selenium.webdriver.chrome.options import Options
LOCAL_DIR = os.getcwd()

# chrome_options = Options()
# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# driver = webdriver.Chrome(
#     executable_path=f'{LOCAL_DIR}\\driver\\geckodriver.exe', options=chrome_options
# )
def browser_option():

    option = FirefoxOptions()
    option.set_preference("general.useragent.override", "Mozilla/5.0 (Series30Plus; Nokia220/10.03.11; Profile/Series30Plus Configuration/Series30Plus) Gecko/20100401 S40OviBrowser/3.8.1.0.5") # Меняем юзерагент "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    option.set_preference('dom.webdriver.enabled',False) # Пытаемся скрыть силениум
    option.set_preference('dom.webnotifications.enabled',False) # Пытаемся скрыть силениум
    option.set_preference('useAutomationExtension', False) # Пытаемся скрыть силениум
    option.set_preference('navigator.webdriver', "undefined") # Пытаемся скрыть силениум
    option.set_preference("javascript.enabled", True)
    option.set_preference('media.volume_scale','0.0') # Выключим звук
    option.set_preference("--disable-infobars",True)
    option.set_preference("--disable-notifications",True)
    option.set_preference('--disable-gpu',True)
    # option.set_capability("deviceName", "IPhone X")
    # option.set_capability("deviceMetrics", { "width": 375, "height": 812, "pixelRatio": 3.0 })
    option.headless = False
    return option

driver = webdriver.Firefox(options=browser_option(),
                        executable_path=f'{LOCAL_DIR}\\driver\\geckodriver.exe')

url = "https://youtube.com/" #"https://t.me/s/testlinkformyproject"  #"https://youtube.com/"
driver.get(url)
time.sleep(.1)
print("end")
# def MobileAgent_random():
#     mobile_agents = []

#     with open(f'{LOCAL_DIR}\\agents.txt', 'r', encoding='utf-8') as file:
#         data = file.read()



#     for line in data.split("\n") :
#         if "iphone" in line or "Nokia" in line or "iPad" in line or "Windows Phone" in line or "Nexus" in line:
#             mobile_agents.append(line)

#     return random.choice(mobile_agents)

# print(MobileAgent_random())