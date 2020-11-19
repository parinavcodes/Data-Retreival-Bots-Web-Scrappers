import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import itertools
from selenium.webdriver.chrome.options import *

url="https://www.naukri.com/content-writing-content-developer-technical-writer-content-editing-copyright-jobs-26?ctcFilter=6to10&ctcFilter=10to15"
pg_num=1

def start_page(pg_num):
    cur_page=1
    if pg_num<=10:
        n=str(pg_num)
        button = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a["+ n +"]")
        driver.implicitly_wait(30000)
        driver.execute_script("arguments[0].click();", button)
        cur_page = int(driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a["+ n +"]").text)
        time.sleep(3)
        return
    while cur_page < pg_num:
        if pg_num>=int(driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a[10]").text):
            button = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a[10]")
            driver.implicitly_wait(30000)
            cur_page = int(driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a[10]").text)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
            # print("cp",cur_page)
        else:
            n=pg_num-cur_page
            t=str(6+n)
            # print("t", t)
            button = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a[" + t + "]")
            driver.implicitly_wait(30000)
            driver.execute_script("arguments[0].click();", button)
            cur_page = int(driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/div/a["+ t +"]").text)
            time.sleep(3)

with open('../naukri_scraper_res.csv', 'a') as f:
     f.write("Company Name" + "," + "Contact Person" + "," + "Email" + "," + "Phone Number" + "," +"Website"+ "\n")
driver=webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe')
driver.get(url)
t_out=5
try:
    element_pres = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[4]/div[2]/section[2]/div[2]//a[@href]'))
    WebDriverWait(driver, t_out).until(element_pres)
except TimeoutException:
    print("Page not loaded")
button=driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[1]/div/span[2]/p")
driver.implicitly_wait(30000)
driver.execute_script("arguments[0].click();", button)
time.sleep(1)
button = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/section[2]/div[1]/div/span[2]/ul/li[2]")
driver.implicitly_wait(30000)
driver.execute_script("arguments[0].click();", button)
time.sleep(2)

while True:
    j = 0
    name = ""
    phnumber = ""
    email = ""
    website = ""
    count =0
    start_page(pg_num)
    comp_links = driver.find_elements_by_xpath('//a[@class="title fw500 ellipsis"]')
    print(len(comp_links))
    for links in comp_links:
        print(links.get_attribute("href"))
        options= Options()
        options.add_argument('--headless')
        driver2 = webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe',options=options)
        driver2.get(links.get_attribute("href"))
        t_out=6
        try:
            element_pres = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[1]/div/a'))
            WebDriverWait(driver2, t_out).until(element_pres)
        except TimeoutException:
            print("Page not loaded")
            j=j+1
            driver2.close()
            continue

        comp_name=driver2.find_element_by_xpath("/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[1]/div/a")
        comp_info_tab=driver2.find_elements_by_xpath('//div[@class="comp-info-detail"]/label')
        comp_info_detail=driver2.find_elements_by_xpath('//div[@class="comp-info-detail"]/span')
        with open('../naukri_scraper_res.csv', 'a') as f:
            for (i,k) in zip(comp_info_tab,comp_info_detail):
                if i.text.lower()=="contact person":
                    name=k.text
                elif i.text.lower()=="phone number":
                    phnumber=k.text
                elif i.text.lower()=="email":
                    email=k.text
                elif i.text.lower()=="website":
                    website=k.text

            f.write(comp_name.text + "," + name + "," + email + "," + phnumber + "," + website + "\n")
            print(comp_name.text + "," + name + "," + email + "," + phnumber + "," + website +"\n")
            name=""
            email=""
            phnumber=""
            website=""
        driver2.close()
        print(j+1)
        j=j+1
    button=driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/section[2]/div[3]/a[2]/span')
    driver.implicitly_wait(30000)
    if button.is_enabled()==True:
        driver.execute_script("arguments[0].click();", button)
    else:
        break
time.sleep(2)
