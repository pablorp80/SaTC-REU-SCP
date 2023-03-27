import os
from os import chdir
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import random as rand
from bs4 import *


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

time.sleep(5)

# working cities, program works for this layout, works best to put in
# one city at a time rather than treating it as a true set
#'sanantonio', 'austin', 'houston','lubbock', 'dallas', 'waco',
# 'newyork', 'losangeles', 'sacramento', 'sfbay', 'lubbock'
wcities = {'dallas'}

# non-working cities, have a different layout
#nwcities = {'detroit', 'chicago', 'stlouis','memphis', 'baltimore', 'milwaukee', }

# number of items, just for testing purposes
count = 1

# make a directory to store the files if it doesn't exist
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir + "/itemdata"
folders = []
if (not os.path.isdir(current_dir)):
    os.mkdir(current_dir)
    folders = []
# get each folder name in the directory
else:
    folders = os.listdir(current_dir)


# iterate through cities
for c in wcities:
    print('NEW CITY: ' + c + '!')
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))

    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    time.sleep(20)
    driver.execute_script("arguments[0].click();", element)

    time.sleep(20)
    allRecorded = True
    doneForCity = False
    pages_skipped = 0
    while (allRecorded):
        try:
            list = driver.find_element(
                By.XPATH, '//*[@id="search-results-page-1"]')
            time.sleep(5)
            html = list.get_attribute("innerHTML")
            soup = BeautifulSoup(html, features="html.parser")
            anchors = soup.findAll('a')

            ids = []
            if (anchors == []):
                print('empty anchor')
            else:
                for a in anchors:
                    # get the id of the item
                    last_slash = a['href'].rfind('/')

                    id = a['href'][last_slash + 1:-5]
                    ids.append(id)
                    if id not in folders:
                        print('NEW ITEM: ' + id)
                        allRecorded = False

            if (allRecorded):
                # get the next page
                pages_skipped += 1
                print('skipped ' + str(pages_skipped) + ' pages')
                try:
                    # get the current url
                    current_url = driver.current_url
                    next_page_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="search-toolbars-1"]/div[2]/button[3]')))

                    driver.execute_script(
                        "arguments[0].click();", next_page_button)

                    # wait for the page to load
                    time.sleep(5)

                    # check if the url changed
                    if (driver.current_url == current_url):
                        doneForCity = True
                        break
                except:
                    break
        except:
            print('couldnt get html')
            break

    if (doneForCity):
        print('All items recorded for ' + c)
        continue

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'titlestring')))
    x = driver.find_element(
        By.CLASS_NAME, 'titlestring')
    # get first element of a city
    driver.execute_script("arguments[0].click();", x)
    prev_link = ""
    cur_link = driver.current_url
    # make sure that the link is changing
    while (cur_link != prev_link):
        # get listing title of item
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="titletextonly"]')))
            title = driver.find_element(
                By.XPATH, '//*[@id="titletextonly"]').text
        except:
            title = 'unknown'
        # get item id
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/section/section/div[2]/p[1]')))
            id = driver.find_element(
                By.XPATH, '/html/body/section/section/section/div[2]/p[1]').text
            id = id.replace('post id: ', '')
        except:
            title = 'unknown'
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/section/section/div[2]/p[2]/time')))
            date = driver.find_element(
                By.XPATH, '/html/body/section/section/section/div[2]/p[2]/time')
            driver.execute_script("arguments[0].click();", date)
            date = date.text
        except:
            date = 'unknown'
        # get price of item
        p = driver.find_elements(
            By.XPATH, '/html/body/section/section/h1/span/span[2]')
        if (p == []):
            price = 'unknown'
        else:
            price = p[0].text
            if (price[0] != '$'):
                price = 'unknown'
        # get the description of the item
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.ID, 'postingbody')))
            d = driver.find_element(
                By.ID, 'postingbody').text
            d = d.replace('show contact info', '')
        except:
            d = 'unknown'

        images = driver.find_elements(By.XPATH, '//img')
        # Extract the URLs of the posting images
        image_urls = [image.get_attribute("src") for image in images]
        # there are some default Craigslist images, logos, maps, etc. that
        # need to be ignored. This function fixes that.

        def get_images(strings):
            return {s for s in strings if s.startswith('https://images.craigslist.org/')}
        image_urls = get_images(image_urls)
        old_dir = current_dir
        current_dir = current_dir + "/" + id
        if (not os.path.isdir(current_dir)):
            os.mkdir(current_dir)

        chdir(current_dir)

        with open("price.txt", 'w+') as f:
            f.write(price)
        with open("title.txt", 'w+') as f:
            f.write(title)
        with open("date.txt", 'w+') as f:
            f.write(date)
        with open("description.txt", 'w+') as f:
            f.write(d)
        with open("city.txt", 'w+') as f:
            f.write(c)

        with open("images.txt", 'w+') as f:
            if (image_urls != set()):
                for each in image_urls:
                    f.write(each + '\n')
            else:
                f.write("no images")

        print(count, end=" ", flush=True)
        count = count + 1
        chdir(old_dir)
        current_dir = old_dir
        # navigate to the 'next' button
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))
        # program is over for this city
        except:
            break
        # move to 'next' button
        ActionChains(driver).move_to_element(driver.find_element(
            By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]'))
        # wait until 'next' button is clickable
        ele = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))
        # click on 'next button' and store previous url
        prev_link = cur_link

        driver.execute_script("arguments[0].click();", ele)
        #time.sleep(rand.uniform(10, 20))
        time.sleep(1)
        cur_link = driver.current_url
driver.quit()
