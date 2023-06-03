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
import random
from itertools import cycle


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

time.sleep(5)


##### WORKING CITIES #####

test_cities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas',
               'waco', 'newyork', 'losangeles', 'sacramento', 'sfbay', 'lubbock', 'phoenix',
               'seattle', 'charlotte', 'denver', 'boston',
               'cleveland', 'minneapolis', 'portland', 'memphis', 'detroit', 'milwaukee',
               'baltimore', 'atlanta', 'tampa', 'wichita', 'lasvegas', 'indianapolis',
               'chicago', 'jacksonville', 'philadelphia', 'nashville', 'elpaso', 'louisville',
               'albuquerque', 'omaha', 'miami', 'orlando', 'stlouis', 'lincoln', 'rochester',
               'boise', 'buffalo', 'madison', 'knoxville', 'springfield', 'syracuse',
               'dayton', 'abilene', 'amarillo', 'delrio', 'elpaso', 'cosprings', 'boulder',
               'fortcollins', 'ogden', 'stgeorge', 'fresno', 'monterey', 'chico', 'merced',
               'reno', 'santabarbara', 'orangecounty', 'palmsprings', 'goldcountry', 'bakersfield'}


## number of items for testing purposes ##
count = 1

##### make itemdata folder if it doesn't exist #####
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir + "/itemdata"
folders = []

if (not os.path.isdir(current_dir)):
    os.mkdir(current_dir)

##### Get each folder name in the directory #####
else:
    folders = os.listdir(current_dir)


################## iterate through cities in a cycle ##################

for c in cycle(test_cities):

    ##### get craigslist auto parts page for current city #####
    print('NEW CITY: ' + c + '!')
    curl = 'https://' + c + '.craigslist.org/search/pta'
    driver.get(curl)

    ##### get list of items, populate id set, scrape if there is a new item #####
    allRecorded = True
    doneForCity = False
    pages_visited = 0
    page_url = ''
    while (allRecorded):
        try:

            ##### get list of items #####

            list = driver.find_element(
                By.XPATH, '//*[@id="search-results-page-1"]')
            time.sleep(5)
            html = list.get_attribute("innerHTML")
            soup = BeautifulSoup(html, features="html.parser")
            anchors = soup.findAll('a')

            ##### populate id set from anchors #####
            id_set = set()
            if (anchors == []):
                print('empty anchor')
            else:
                for a in anchors:

                    ##### extract id #####
                    url = a['href']
                    id_start_index = url.rfind('/') + 1
                    id_end_index = id_start_index + 10
                    ten_digit_id = url[id_start_index:id_end_index]

                    ##### add id to set #####
                    id_set.add(ten_digit_id)
                    if ten_digit_id not in folders:
                        print('new item found: ' + ten_digit_id)
                        allRecorded = False

            ##### if all items aren't recorded, add new items #####
            if (not allRecorded):
                page_url = driver.current_url

                for i in id_set:

                    ######## check if the item is already recorded ########
                    if (i not in folders):

                        ######## mark the item as scraped ########
                        folders.append(i)

                        ################## go to the url of the item ##################

                        url = 'https://' + c + '.craigslist.org/pts/' + i + '.html'
                        driver.get(url)
                        # sleep random uniform time betwen 10 and 20 seconds
                        #time.sleep(rand.uniform(10, 20))
                        time.sleep(2)

                        ################## check if the item exists ##################
                        title_test = driver.find_elements(
                            By.XPATH, '/html/body/div/header/nav/ul/li/p')

                        if (title_test != []):
                            ##### if it doesn't exist, go to next item #####
                            if (title_test[0].text == 'Page Not Found'):
                                continue

                        ################## get item title ##################

                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="titletextonly"]')))
                            title = driver.find_element(
                                By.XPATH, '//*[@id="titletextonly"]').text
                        except:
                            title = 'unknown'

                        ################## get item id ##################
                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.XPATH, '/html/body/section/section/section/div[2]/p[1]')))
                            id = driver.find_element(
                                By.XPATH, '/html/body/section/section/section/div[2]/p[1]').text
                            id = id.replace('post id: ', '')
                        except:
                            title = 'unknown'

                        ################## get item posting date ##################

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

                        ################## get item price ##################

                        p = driver.find_elements(
                            By.XPATH, '/html/body/section/section/h1/span/span[2]')
                        if (p == []):
                            price = 'unknown'
                        else:
                            price = p[0].text
                            if (price[0] != '$'):
                                price = 'unknown'

                        ################## get item description ##################

                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                                (By.ID, 'postingbody')))
                            d = driver.find_element(
                                By.ID, 'postingbody').text
                            d = d.replace('show contact info', '')
                        except:
                            d = 'unknown'

                        ################## get item images ##################

                        images = driver.find_elements(By.XPATH, '//img')
                        # Extract the URLs of the posting images
                        image_urls = [image.get_attribute(
                            "src") for image in images]
                        # there are some default Craigslist images, logos, maps, etc. that
                        # need to be ignored. This function fixes that.

                        def get_images(strings):
                            return {s for s in strings if s.startswith('https://images.craigslist.org/')}

                        image_urls = get_images(image_urls)

                        ################## save item data to file ##################

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

                        ################## print item count for testing ##################
                        print(count, end=" ", flush=True)
                        count = count + 1

                        ######## go back to itemdata directory ########

                        chdir(old_dir)
                        current_dir = old_dir

                #### go back to the listing page once all items have been scraped #####
                driver.get(page_url)

                time.sleep(10)

                ########## go to the next page of items if there is one ##########

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

                    ##### check if the new url is a new page #####
                    if (driver.current_url == current_url):
                        doneForCity = True
                        print('done for city')
                        break

                    ##### if the button changed the url, go to the next page #####
                    else:
                        allRecorded = True
                except:
                    break

            else:
                pages_visited += 1
                print('visited ' + str(pages_visited) + ' pages')
                try:
                    #### get current url ####
                    current_url = driver.current_url

                    ## get next page url (or what it would be if there was one) ##
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

                    ##### check if the new link changed the url #####
                    if (driver.current_url == current_url):
                        doneForCity = True
                        print('done for city')
                        break

                    # if the url didn't change, go to next city. The way craigslist
                    # does this is that if you put in a page number that doesn't exist, it
                    # will redirect you to the page directly before it. So in this case, we get the
                    # URL, try to put in the URL of the next page, and if it sends us back to the URL
                    # we were just at, we know that there are no more pages #####
                    else:
                        allRecorded = True
                except:
                    break
        except:
            print('couldnt get html')
            break
