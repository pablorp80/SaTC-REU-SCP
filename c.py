from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from bs4 import BeautifulSoup
from os import chdir
from selenium.webdriver.chrome.service import Service
import random as rand
from itertools import cycle


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


time.sleep(5)

#'sanantonio', 'austin', 'houston','lubbock', 'dallas', 'waco',
# 'newyork', 'losangeles', 'sacramento', 'sfbay', 'lubbock', 'phoenix', 'seattle', 'charlotte', 'denver', 'boston', 'cleveland'
# 'minneapolis', 'portland'
test_cities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas'
               , 'waco', 'newyork', 'losangeles', 'sacramento', 'sfbay', 
               'lubbock', 'phoenix', 'seattle', 'charlotte', 'denver', 
               'boston', 'cleveland', 'minneapolis', 'portland'}

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


################## ITERATE THROUGH CITIES ##################


for c in cycle(test_cities):
    print('NEW CITY: ' + c + '!')
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))

    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    time.sleep(5)
    driver.execute_script("arguments[0].click();", element)

    # wait for the page to load
    time.sleep(5)

    allRecorded = True
    doneForCity = False
    pages_visited = 0
    items_map = {}
    page_url = ''
    while (allRecorded):
        try:
            list = driver.find_element(
                By.XPATH, '//*[@id="search-results-page-1"]')
            time.sleep(5)
            html = list.get_attribute("innerHTML")
            soup = BeautifulSoup(html, features="html.parser")
            anchors = soup.findAll('a')

            id_set = set()
            if (anchors == []):
                print('empty anchor')
            else:
                for a in anchors:
                    # get the id of the item
                    url = a['href']

                    # Extract the ten-digit ID
                    id_start_index = url.rfind('/') + 1
                    id_end_index = id_start_index + 10
                    ten_digit_id = url[id_start_index:id_end_index]

                    id_set.add(ten_digit_id)
                    if ten_digit_id not in folders:
                        print('new item found: ' + ten_digit_id)
                        allRecorded = False

            if (not allRecorded):
                page_url = driver.current_url
                for i in id_set:
                    if (i not in folders):
                        folders.append(i)
                        url = 'https://' + c + '.craigslist.org/pts/' + i + '.html'
                        driver.get(url)
                        time.sleep(.2)

                        title_test = driver.find_elements(
                            By.XPATH, '/html/body/div/header/nav/ul/li/p')

                        if (title_test != []):
                            if (title_test[0].text == 'Page Not Found'):
                                continue

                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="titletextonly"]')))
                            title = driver.find_element(
                                By.XPATH, '//*[@id="titletextonly"]').text
                        except:
                            title = 'unknown'

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
                            driver.execute_script(
                                "arguments[0].click();", date)
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
                        image_urls = [image.get_attribute(
                            "src") for image in images]
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

                # want to be able to go to next page from current page
                driver.get(page_url)

                pages_visited += 1
                print('visited ' + str(pages_visited) + ' pages')
                try:
                    # get the current url
                    current_url = driver.current_url

                    # get the next page button
                    try:
                        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                            (By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[2]/button[3]')))

                        next_page_button = driver.find_element(
                            By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[2]/button[3]')
                    except:
                        print('no next page button')

                    # click the next page button
                    driver.execute_script(
                        'arguments[0].click()', next_page_button)

                # wait for the page to load
                    time.sleep(15)

                # check if the url changed

                    if (driver.current_url == current_url):
                        # try to click the next page button again
                        driver.execute_script(
                            'arguments[0].click()', next_page_button)
                        time.sleep(15)

                    if (driver.current_url == current_url):
                        doneForCity = True
                        print('done for city')
                        break
                    else:
                        allRecorded = True
                except:
                    break

            else:
                print('all recorded for page')
        except:
            print('couldnt get html')
            break
