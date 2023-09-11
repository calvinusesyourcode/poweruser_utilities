from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Specify the URL and driver
url = 'https://www.facebook.com'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

email = "calvinducharme@gmail.com"
password = "suckth3Zuck!"

driver.find_element("id","email").send_keys(email)
driver.find_element("id","pass").send_keys(password)
driver.find_element("name","login").click()
time.sleep(15)




url = "https://www.facebook.com/marketplace/112008808810771/search?query=quest%202"
driver.get(url)

# Option 2 - Script click
print(driver.page_source)
time.sleep(30)