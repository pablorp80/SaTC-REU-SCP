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


##### WORKING CITIES #####
# test_cities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas', 'waco', 'newyork', 'losangeles', 'sacramento', 'sfbay', 'lubbock', 'phoenix',
#                'seattle', 'charlotte', 'denver', 'boston',
#                'cleveland', 'minneapolis', 'portland'}

test_cities = {'waco', 'lubbock'}


## NUMBER OF ITEMS, JUST FOR TESTING PURPOSES ##
count = 1

##### MAKE ITEMDATA FOLDER IF IT DOESN'T EXIST #####
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir + "/itemdata"
folders = []

## IF ITEMDATA FOLDER DOESN'T EXIST, MAKE IT ##
if (not os.path.isdir(current_dir)):
    os.mkdir(current_dir)

##### GET EACH FOLDER NAME IN THE DIRECTORY #####
else:
    folders = os.listdir(current_dir)


################## ITERATE THROUGH CITIES IN A CYCLE ##################

for c in cycle(test_cities):

    ##### GET CRAIGSLIST AUTO PARTS PAGE FOR CITY #####
    print('NEW CITY: ' + c + '!')
    curl = 'https://' + c + '.craigslist.org/search/pta'
    driver.get(curl)

    ##### GET LIST OF ITEMS, POPULATE ID SET, SCRAPE IF NEW ITEM #####
    allRecorded = True
    doneForCity = False
    pages_visited = 0
    page_url = ''
    while (allRecorded):
        try:

            ##### GET LIST OF ITEMS #####

            list = driver.find_element(
                By.XPATH, '//*[@id="search-results-page-1"]')
            time.sleep(5)
            html = list.get_attribute("innerHTML")
            soup = BeautifulSoup(html, features="html.parser")
            anchors = soup.findAll('a')

            ##### POPULATE ID SET FROM ANCHORS #####
            id_set = set()
            if (anchors == []):
                print('empty anchor')
            else:
                for a in anchors:

                    ##### EXTRACT ID #####
                    url = a['href']
                    id_start_index = url.rfind('/') + 1
                    id_end_index = id_start_index + 10
                    ten_digit_id = url[id_start_index:id_end_index]

                    ##### ADD ID TO SET #####
                    id_set.add(ten_digit_id)
                    if ten_digit_id not in folders:
                        print('new item found: ' + ten_digit_id)
                        allRecorded = False

            ##### IF ALL ITEMS AREN'T RECORDED, SCRAPE THE NEW ITEMS #####
            if (not allRecorded):
                page_url = driver.current_url

                for i in id_set:

                    ######## CHECK IF ITEM IS ALREADY RECORDED ########
                    if (i not in folders):

                        ######## MARK ITEM AS SCRAPED ########
                        folders.append(i)

                        ################## GO TO ITEM URL ##################

                        url = 'https://' + c + '.craigslist.org/pts/' + i + '.html'
                        driver.get(url)
                        # sleep random uniform time betwen 10 and 20 seconds
                        #time.sleep(rand.uniform(10, 20))
                        time.sleep(2)

                        ################## CHECK IF ITEM EXISTS ##################
                        title_test = driver.find_elements(
                            By.XPATH, '/html/body/div/header/nav/ul/li/p')

                        if (title_test != []):
                            ##### IF ITEM DOESN'T EXIST, CONTINUE TO NEXT ITEM #####
                            if (title_test[0].text == 'Page Not Found'):
                                continue

                        ################## GET ITEM TITLE ##################

                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="titletextonly"]')))
                            title = driver.find_element(
                                By.XPATH, '//*[@id="titletextonly"]').text
                        except:
                            title = 'unknown'

                        ################## GET ITEM ID ##################
                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.XPATH, '/html/body/section/section/section/div[2]/p[1]')))
                            id = driver.find_element(
                                By.XPATH, '/html/body/section/section/section/div[2]/p[1]').text
                            id = id.replace('post id: ', '')
                        except:
                            title = 'unknown'

                        ################## GET ITEM POSTING DATE ##################

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

                        ################## GET ITEM PRICE ##################

                        p = driver.find_elements(
                            By.XPATH, '/html/body/section/section/h1/span/span[2]')
                        if (p == []):
                            price = 'unknown'
                        else:
                            price = p[0].text
                            if (price[0] != '$'):
                                price = 'unknown'

                        ################## GET ITEM DESCRIPTION ##################

                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.ID, 'postingbody')))
                            d = driver.find_element(
                                By.ID, 'postingbody').text
                            d = d.replace('show contact info', '')
                        except:
                            d = 'unknown'

                        ################## GET ITEM IMAGES ##################

                        images = driver.find_elements(By.XPATH, '//img')
                        # Extract the URLs of the posting images
                        image_urls = [image.get_attribute(
                            "src") for image in images]
                        # there are some default Craigslist images, logos, maps, etc. that
                        # need to be ignored. This function fixes that.

                        def get_images(strings):
                            return {s for s in strings if s.startswith('https://images.craigslist.org/')}

                        image_urls = get_images(image_urls)

                        ################## SAVE ITEM DATA TO FILE ##################

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

                        ################## PRINT COUNT FOR TESTING ##################
                        print(count, end=" ", flush=True)
                        count = count + 1

                        ######## GO BACK TO ITEMDATA DIRECTORY ########

                        chdir(old_dir)
                        current_dir = old_dir

                #### GO BACK TO THE ITEM LISTING PAGE ONCE ALL ITEMS HAVE BEEN SCRAPED #####
                driver.get(page_url)

                time.sleep(10)

                ########## GO TO THE NEXT PAGE IF THERE IS ONE ##########

                pages_visited += 1
                print('visited ' + str(pages_visited) + ' pages')
                try:
                    #### GET CURRENT URL ####
                    current_url = driver.current_url

                    ## Get next page URL ##
                    try:
                        def find_second_instance(string, char='~'):
                            first_instance = string.find(char)
                            if first_instance == -1:
                                return -1

                            second_instance = string.find(
                                char, first_instance + 1)
                            return second_instance

                        position = find_second_instance(current_url)

                    # Exract the first "0" after the found position
                        number = int(current_url[position + 1])

                    # Increment the number
                        number += 1

                    # Replace the old number with the incremented number in the URL
                        new_url = current_url[:position + 1] + \
                            str(number) + current_url[position + 2:]
                    except:
                        print('new page failed')

                    driver.get(new_url)

                    time.sleep(15)

                    ##### CHECK IF THE NEW URL IS A NEW PAGE #####
                    if (driver.current_url == current_url):
                        doneForCity = True
                        print('done for city')
                        break

                    ##### IF THE BUTTON DID CHANGE THE URL, CONTINUE TO THE NEXT PAGE #####
                    else:
                        allRecorded = True
                except:
                    break

            else:
                pages_visited += 1
                print('visited ' + str(pages_visited) + ' pages')
                try:
                    #### GET CURRENT URL ####
                    current_url = driver.current_url

                    ## GET NEXT PAGE URL ##
                    try:

                        def find_second_instance(string, char='~'):
                            first_instance = string.find(char)
                            if first_instance == -1:
                                return -1

                            second_instance = string.find(
                                char, first_instance + 1)
                            return second_instance

                        position = find_second_instance(current_url)

                    # Exract the first "0" after the found position
                        number = int([position + 1])

                    # Increment the number
                        number += 1

                    # Replace the old number with the incremented number in the URL
                        new_url = url[:position + 1] + \
                            str(number) + url[position + 2:]
                    except:
                        print('no next page button')

                    driver.get(new_url)

                    time.sleep(15)

                    ##### CHECK IF THE NEXT PAGE BUTTON CHANGED THE URL #####
                    if (driver.current_url == current_url):
                        doneForCity = True
                        print('done for city')
                        break

                    ##### IF THE BUTTON DID CHANGE THE URL, CONTINUE TO THE NEXT PAGE #####
                    else:
                        allRecorded = True
                except:
                    break
        except:
            print('couldnt get html')
            break

