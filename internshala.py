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

search="Content Writing"

options=Options()
options.add_argument("--disable-notifications")
driver=webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe',options=options)
driver.get("https://internshala.com/")
driver.find_element_by_xpath('//div[@class="input-group has_cross_and_button"]/input').click()
time.sleep(1)
driver.find_element_by_xpath('//input[@class="form-control ui-autocomplete-input"]').send_keys(search)
time.sleep(1.5)
driver.find_element_by_xpath('//button[@id="internship_search_button"]').click()
pn=0
t_out=5
try:
    element_pres = EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[17]/div/div[2]/div[3]/div[2]'))
    WebDriverWait(driver, t_out).until(element_pres)
except TimeoutException:
    print("Pop up not loaded")
    pn=1
if pn==0:
    driver.find_element_by_xpath('//*[@id="wrapper"]/div[17]/div/div[2]/div[3]/div[2]').click()
    time.sleep(1)

with open('internshala_scraper_res.csv','a') as f:
    f.write("Company Name"+","+"Link"+","+"Stipend"+"\n")

total_page=int(driver.find_element_by_xpath('//span[@id="total_pages"]').text)

for i in range(total_page-1):
    j=str(i+1)
    int_list = driver.find_elements_by_xpath('//div[@id="internship_list_container_' + j + '"]/div')
    for post in int_list:
        comp_name=post.find_element_by_xpath('./div/div/div//div[@class="heading_6 company_name"]//a[@href]')
        job_name=post.find_element_by_xpath('./div/div/div//div[@class="heading_4_5 profile"]/a')
        stp=post.find_element_by_xpath('./div/div/div/div/div//span[@class="stipend"]')
        print(comp_name.text)
        print(job_name.get_attribute("href"))
        print(stp.text)
        with open('internshala_scraper_res.csv','a') as f:
            f.write(comp_name.text + "," + job_name.get_attribute("href") + "," + stp.text +"\n")
    driver.find_element_by_xpath('//a[@class="next_page hideUndoOnClick"]').click()
    time.sleep(3)
