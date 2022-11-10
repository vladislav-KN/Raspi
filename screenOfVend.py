import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/usr/lib/chromium-browser/chromium-browser"    #chrome binary location specified here
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
driver.get('https://192.168.1.102/VendingSys_Server/VendingWindow/1')

print("sleep...")
time.sleep(60)
print("Refresh!")
driver.refresh()
print("Refreshed!")
