import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import *
import unidecode

options= Options()
options.add_argument("--disable-notifications")
driver= webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe',options=options)
driver.get("https://www.reddit.com/r/HireaWriter/new/")
t_out=7

try:
    element_pres = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[1]/div[4]/div/button'))
    WebDriverWait(driver, t_out).until(element_pres)
except TimeoutException:
    print("Page not loaded")


time.sleep(5)
last_height=0
new_height=0

with open('reddit_scraped_results.csv','a') as f:
    f.write("Title"+","+"Author Link"+"\n")
for i in range(125):
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("nh:",new_height)
    print("lh:",last_height)
    driver.execute_script("window.scrollTo("+str(new_height)+","+str(last_height)+");")
    time.sleep(5)
    new_height = last_height

driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(5)
info = driver.find_elements_by_xpath('//div[@class="_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 "]')
links = driver.find_elements_by_xpath('//div[@class="_3AStxql1mQsrZuUIFP9xSg nU4Je7n-eSXStTBAPMYt8"]')
print(len(links))
print(len(info))

for i in range(0,len(links)):
    print(i)
    if links[i].text.lower().count('promoted')==1:
        continue
    try:
        a_link=links[i].find_element_by_xpath('./div//a[@href]')
    except NoSuchElementException:
        print("exception: user link not found")
        continue
    try:
        head = info[i].find_element_by_xpath('./div//div[@class="_2xu1HuBz1Yx6SP10AGVx_I"]')
    except NoSuchElementException:
        print("exception:heading not found")
        continue
    a_link=links[i].find_element_by_xpath('./div//a[@href]')
    head=info[i].find_element_by_xpath('./div//div[@class="_2xu1HuBz1Yx6SP10AGVx_I"]')
    title=info[i].find_element_by_xpath('.//div[@class="y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE"]')
    driver.execute_script("arguments[0].scrollIntoView();", head)
    if head.text.lower().count('hiring')!=0:
        if unidecode.unidecode(title.text) == title.text:
            with open('reddit_scraper_results.csv','a') as f:
                f.write(title.text + "," + a_link.get_attribute("href") +"\n")
                print(head.text)
                print(title.text)
                print(a_link.get_attribute("href"))
                print(links[i].find_element_by_xpath('.//a[@class="_3jOxDPIQ0KaOWpzvSQo-1s"]').text)