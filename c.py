import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(ChromeDriverManager().install())

time.sleep(5)
# both lists subject to change, but must be the actual craigslist title

# working cities, program works for this layout, works best to put in
# one city at a time rather than treating it as a true set

#'sanantonio', 'austin', 'houston','lubbock', 'dallas', 'waco',
# 'newyork', 'losangeles', 'sacramento', 'sfbay'
wcities = {'lubbock', 'waco'}

# non-working cities, have a different layout
#nwcities = {'detroit', 'chicago', 'stlouis','memphis', 'baltimore', 'milwaukee', }

# number of items, just for testing purposes
count = 1

for c in wcities:
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))
    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    element.click()

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

        i = driver.find_elements(By.TAG_NAME, 'img')

        if (i == []):
            print('no images here')

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
            # 'show contact info' can be added to a description
            # as a button so a buyer can contact the seller. The name
            # of this button, however, is interpreted as a string and
            # should be ignored in this case
            d = d.replace('show contact info', '')
        except:
            d = 'unknown'

        # print data to terminal for now
        print(count)
        images = driver.find_elements(By.XPATH, '//img')

        # Extract the URLs of the posting images
        image_urls = [image.get_attribute("src") for image in images]

        # there are some default Craigslist images, logos, maps, etc. that
        # need to be ignored. This function fixes that.
        def get_images(strings):
            return {s for s in strings if s.startswith('https://images.craigslist.org/')}

        image_urls = get_images(image_urls)

        print('{DATE:   ' + date + '}')
        print('{ID:     ' + id + '}')
        print('{PRICE:  ' + price + '}')
        print('{TITLE:  ' + title + '}')
        print('{REGION: ' + c + '}')
        print('DESCRIPTION: \n' + d + '\n')

        # Print the image URLs if there are any photos
        if (image_urls != set()):
            print('IMAGE LINKS: \n')
            print(image_urls)
        print('\n\n\n\n')
        count = count + 1

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
        # sleeping for 1 second has been enough to not get flagged
        time.sleep(1)
        driver.execute_script("arguments[0].click();", ele)
        cur_link = driver.current_url
