from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
#object of Options class
op = webdriver.ChromeOptions()
#add user Agent
op.add_argument
("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
+"AppleWebKit/537.36 (KHTML, like Gecko)"
+"Chrome/87.0.4280.141 Safari/537.36")
#set chromedriver.exe path
driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe",
options=op)
#maximize browser
driver.maximize_window()
#launch URL
driver.get("https://vancouver.craigslist.org/rds/vgm/d/langley-vr-oculus-quest-headset-plus/7621209927.html")
# Target the button element
button_selector = 'button.reply-button'
button = driver.find_element(By.CSS_SELECTOR, button_selector)

# Option 1 - Click
button.click()
WebDriverWait(driver,timeout=10).until(lambda doc: doc.find_element(By.CLASS_NAME,"reply-content"))

# Option 2 - Script click
reply_content = driver.find_element(By.CLASS_NAME, "cl-reply-flap").find_elements(By.CSS_SELECTOR,'*')

for each in reply_content:
    attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', each)
    print(attrs)
#close browser session
driver.quit()