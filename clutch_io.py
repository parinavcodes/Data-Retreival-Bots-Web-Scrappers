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
from selenium.webdriver.common.action_chains import ActionChains


url="https://clutch.co/agencies/digital-marketing?sort_by=1&min_project_size=&avg_hrly_rate=&employees=&client_focus=&industry_focus=&location%5Bcountry%5D=&form_id=spm_exposed_form&form_token=OGDM2bU7aS3RTMwI8ITEJDN0LJe9SwMzVSHZX7Hc5pk&form_build_id=form-HFLesrbbTkN6ll2EfdQWgJX2WAH-izQ322gXhTwHyRI"
pg_num=15
url_chg=""
pg_num=str(pg_num-1)
f=1
if int(pg_num)>=1:
    for c in url:
        url_chg=''.join([url_chg,c])
        if c=='?' and f==1:
            url_chg=''.join([url_chg,"page="+ pg_num +"&"])
            f=0
else:
    url_chg=url
options=Options()
options.add_argument("--disable-notifications")
driver=webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe',options=options)
driver.get(url_chg)
time.sleep(5)
cc=0
t_out=5
try:
    element_pres = EC.presence_of_element_located((By.XPATH, '//a[@id="CybotCookiebotDialogBodyButtonAccept"]'))
    WebDriverWait(driver, t_out).until(element_pres)
except TimeoutException:
    print("Pop up not loaded")
    cc=1
if cc==0:
    cookie_close=driver.find_element_by_xpath('//a[@id="CybotCookiebotDialogBodyButtonAccept"]').click()
filter_tab=driver.find_element_by_xpath('//div[@class="form-type-select form-item-sort-by form-item form-group"]/div/a[@class="chosen-single"]')
filter_tab.click()
time.sleep(1)
opt=driver.find_element_by_xpath('//div/ul//li[@data-option-array-index="3"]')
opt.click()
time.sleep(3)
with open('../clutch_scraper_res.csv', 'a') as f:
    f.write("Company Name,Link,Website,Details\n")

last_page=driver.find_element_by_xpath('//li[@class="pager-last"]/a')
pg_url=str(last_page.get_attribute("href"))
c=0
lp=""
for i in range(len(pg_url)):
    if pg_url[i]=='p' and pg_url[i+1]=='a' and pg_url[i+2]=='g' and pg_url[i+3]=='e' and pg_url[i+4]=='=':
        c=i+5
    if i==c and ord(pg_url[i])>=48 and ord(pg_url[i])<=57:
        lp="".join([lp,pg_url[i]])
        c+=1
lp=int(lp)
print(lp)
ap=0
for i in range(lp):
    comps=driver.find_elements_by_xpath('//ul//li[@class="provider-row"]')
    j=str(i+2)
    ap=0
    print(i)
    for comp in comps:
        if comp.text.count("Need Help Selecting a Company?")==1:
                continue

        comp_details=""
        comp_name=comp.find_element_by_xpath('.//h3[@class="company-name"]/a')
        comp_info=comp.find_elements_by_xpath('.//div[@class="module-list"]/div')
        website=comp.find_element_by_xpath('.//a[@class="sl-ext"]')

        for i in comp_info:
            comp_details="||".join([comp_details,i.text])
        comp_details=comp_details.replace(',','',1)
        comp_details=comp_details.replace(',','-')
        print(comp_name.text +" , "+comp_name.get_attribute("href")+" , "+website.get_attribute("href")+" , "+comp_details+" \n")
        if unidecode.unidecode(comp_details) == comp_details and unidecode.unidecode(comp_name.text) == comp_name.text:
            with open('../clutch_scraper_res.csv', 'a') as f:
                f.write(comp_name.text +","+comp_name.get_attribute("href")+","+website.get_attribute("href")+","+comp_details+"\n")

    action = ActionChains(driver)
    button=driver.find_element_by_xpath('//ul[@class="pagination"]/li//a[@title="Go to page '+ j +'"]')
    action.move_to_element(button).perform()
    driver.implicitly_wait(30000)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
