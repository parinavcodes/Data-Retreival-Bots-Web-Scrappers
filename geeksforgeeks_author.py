import selenium
import csv
import time
import os
import sys
import re
import unidecode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions


def url_generator(inst_links, sn):
    for i in range(sn, len(inst_links)):
        print(len(inst_links))
        res1 = bool(re.search(r"\s", inst_links[i].text))
        if res1 == 1:
            res = inst_links[i].text.lower().replace(" ", "-").replace("y(", "y (").replace(" ", "-").replace("(",
                                                                                                              "").replace(
                ")", "").replace("&", "and").replace("--", "-")
            print(res)
            if res == "birla-institute-of-technology-and-science,-pilani-bits-pilani":
                return "https://auth.geeksforgeeks.org/college/bits-pilani/"
            elif res == "birla-institute-of-technology,-mesra-bit-mesra":
                return "https://auth.geeksforgeeks.org/college/bit-mesra/"
            elif special_char_check(res) == 1:
                return "https://auth.geeksforgeeks.org/college/" + res + "/"
            else:
                continue


def special_char_check(string):
    if unidecode.unidecode(string) == string:
        return 1
    else:
        return 0


def link_finder(elems_linker, cn, ent):
    n_itr = int(cn / 4)
    n_itr = n_itr - 1
    count = 0
    for elems in elems_linker:
        while ent > 0:
            ent = ent - 1
            n_itr = n_itr + 1
        else:
            if count == n_itr:
                link_art = elems.get_attribute("href")
                link_art = link_art.replace('practice', 'articles')
                return link_art
        count = count + 1


def m_pages(max_pge):
    count = 1
    for l in max_pge:
        # print(l.text)
        if l.text == "chevron_right":
            # print(max_pge[count-2].text)
            return (max_pge[count - 2].text)
        else:
            count = count + 1


# with open('opt6.csv','a') as f:
#      f.write("Name" +"," + "Articles URL" +"," +" Article_link \n")

first = 1
first_site = 1
site = 0
exit_n = 0
for pg_num in range(0, 48):
    driver = webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe')
    url_num = str(pg_num)
    req_url = "https://auth.geeksforgeeks.org/colleges/" + url_num + "/"

    driver.get(req_url)

    t_out = 10
    try:
        element_pres = EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div/main/div/div/div[1]/table/tbody'))
        WebDriverWait(driver, t_out).until(element_pres)
    except TimeoutException:
        print("Timed out waiting for page to load")
        continue
    if first_site != 1:
        site = 0
    first_site = 0
    inst_links = driver.find_elements_by_xpath("/html/body/div[2]/div/main/div/div/div[1]/table/tbody//a[@href]")
    for links in range(site, len(inst_links)):
        if first != 1:
            driver.get(req_url)
            t_o = 10
            try:
                element_pr = EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/main/div/div/div[1]/table/tbody'))
                WebDriverWait(driver, t_o).until(element_pr)
            except TimeoutException:
                print("Timed out waiting for page to load")
                continue
        first = 0
        inst_links = driver.find_elements_by_xpath("/html/body/div[2]/div/main/div/div/div[1]/table/tbody//a[@href]")
        if exit_n == 0:
            check_link = url_generator(inst_links, site)
        else:
            site = site + 1
            exit_n = 0
            continue
        site = site + 1
        # time.sleep(1)
        if check_link.count("https://auth.geeksforgeeks.org/college") == 1:
            # print(check_link)
            driver.get(check_link)
            # time.sleep(1)
            timeout = 15
            exit_name = driver.title
            if exit_name == "404 | GeeksforGeeks":
                continue
            try:
                element_present = EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/main/div[3]/div/div[2]/div/ul'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
                continue
            exit_code = driver.find_element_by_xpath("/html/body/div[2]/div/main/div[1]/div/div[2]/div[2]/div/div[3]")
            if exit_code.text == "Campus Ambassador: None":
                print(exit_code.text)
                exit_n = 0
            else:
                exit_n = 1
            '''
            for b in exit_code:
                if b.get_attribute("href") == "https://auth.geeksforgeeks.org":
                        exit_n=1
                        break
            if exit_n==1:
                continue
            '''
            # driver.implicitly_wait(200)
            # for One Institute
            # max_page for finding last page number
            time.sleep(1)
            max_page = driver.find_elements_by_xpath("/html/body/div[2]/div/main/div[3]/div/div[2]/div/ul/li")
            # driver.implicitly_wait(100)
            mpg = m_pages(max_page)

            max_page_num = int(mpg)
            first = 0

            j = 3
            for i in range(max_page_num):
                print(f'page {i + 1}')
                elems_link = driver.find_elements_by_xpath(
                    "/html/body/div[2]/div/main/div[3]/div/div[2]/table/tbody//a[@href]")
                '''
                for elem in elems_link:
                    print(elem.get_attribute("href"))
                '''
                print(len(elems_link))

                element = driver.find_elements_by_xpath('//tr[@class="student-row"]/td')

                # print(nav_button.text)
                # curr_page=nav_button[1].text
                time.sleep(0.70)
                c = 0
                entry = 0
                with open('../opt6.csv', 'a') as f:
                    for i in range(len(element)):
                        c = c + 1
                        if c % 4 == 0 and element[i].text != '-':
                            link_rec = link_finder(elems_link, c, entry)
                            driver2 = webdriver.Chrome(executable_path='D:\drivers\chromedriver.exe')
                            driver2.get(link_rec)
                            t_bout = 10
                            try:
                                element_p = EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[2]/div/main/div[4]/div/section[1]/div/div/ol'))
                                WebDriverWait(driver2, t_bout).until(element_p)
                            except TimeoutException:
                                print("Timed out waiting for page to load")
                                continue
                            article_list = driver2.find_elements_by_xpath('//li[@class="contribute-li"]/a')
                            article_links = driver2.find_elements_by_xpath(
                                "/html/body/div[2]/div/main/div[4]/div/section[1]/div/div/ol//a[@href]")
                            count_1 = 0
                            for art_link in article_links:
                                if special_char_check(article_list[count_1].text) == 1:
                                    f.write(element[i - 3].text + ",  " + art_link.get_attribute("href") + ", " +
                                            article_list[count_1].text + " \n")
                                    print(element[i - 3].text + ",   " + art_link.get_attribute("href") + " ," +
                                          article_list[count_1].text + " \n")
                                else:
                                    count_1 = count_1 + 1
                                    continue
                                count_1 = count_1 + 1
                            entry = entry + 1
                            driver2.close()
                print(f'page{i + 1} done')
                f.close()
                t = j
                k = str(t)
                t_bout = 5
                try:
                    element_p = EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[2]/div/main/div[3]/div/div[2]/div/ul'))
                    WebDriverWait(driver, t_bout).until(element_p)
                except TimeoutException:
                    print("Timed out waiting for page to load")
                    continue
                button = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/main/div[3]/div/div[2]/div/ul/li[" + k + "]/a")
                driver.implicitly_wait(30000)
                driver.execute_script("arguments[0].click();", button)
                if j <= 8:
                    j = j + 1

    driver.close()
