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

url="https://twitter.com/search?q=content%20writer%20needed&src=typed_query&f=live"
driver=webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe')
driver.get(url)
t_out=5
try:
    element_pres = EC.presence_of_element_located((By.XPATH, '//div[@class="css-901oao r-1awozwy r-13gxpu9 r-6koalj r-18u37iz r-16y2uox r-1qd0xha r-a023e6 r-vw2c0b r-1777fci r-eljoum r-dnmrzs r-bcqeeo r-q4m81j r-qvutc0"]'))
    WebDriverWait(driver, t_out).until(element_pres)
except TimeoutException:
    print("Page not loaded")
with open('../twitter.csv', 'a') as f:
    f.write("Name,Link,Post\n")
new_height=0

time.sleep(2)

while True:
    tweets = driver.find_elements_by_xpath('//div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-1mi0q7o"]')
    print(len(tweets))
    for tweet in tweets:
            handle_link=tweet.find_element_by_xpath('.//a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]')
            handle_name=tweet.find_element_by_xpath('.//a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]//div[@class="css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs"]')
            post=tweet.find_element_by_xpath('.//div[@class="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"]')
            print(handle_name.text)
            print(handle_link.get_attribute("href"))
            print(post.text)
            post_refine=post.text.replace(","," ")
            print(post_refine)
            if unidecode.unidecode(post.text)==post.text and unidecode.unidecode(handle_name.text)==handle_name.text:
                with open('../twitter.csv', 'a') as f:
                    f.write(handle_name.text +","+handle_link.get_attribute("href")+","+post_refine+"\n")

    last_height = driver.execute_script("return document.body.scrollHeight")
    print("nh:",new_height)
    print("lh:",last_height)
    driver.execute_script("window.scrollTo("+str(new_height)+","+str(last_height)+");")
    time.sleep(5)
    new_height = last_height