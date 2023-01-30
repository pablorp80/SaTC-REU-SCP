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

#'sanantonio', 'austin', 'houston','lubbock', 'dallas', 'waco', 'newyork'
wcities = {'lubbock'}

# non-working cities, have a different layout
nwcities = {'detroit', 'chicago', 'stlouis',
            'memphis', 'baltimore', 'milwaukee'}

item1 = '//*[@id="search-results-page-1"]/ol/ol/ol[1]/li[1]/div/a'

# number of items, just for testing purposes
count = 1

for c in wcities:
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))
    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    time.sleep(5)
    element.click()

    time.sleep(10)

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, item1)))

    x = driver.find_element(
        By.XPATH, item1)

    # get first element of a city
    driver.execute_script("arguments[0].click();", x)

    prev_link = ""
    cur_link = driver.current_url

    # make sure that the link is changing
    while (cur_link != prev_link):
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="titletextonly"]')))
        except:
            cur_link = driver.current_url
            continue

        title = driver.find_element(
            By.XPATH, '//*[@id="titletextonly"]').text

        p = driver.find_elements(
            By.XPATH, '/html/body/section/section/h1/span/span[2]')

        if (p == []):
            price = 'unknown'
        else:
            price = p[0].text
            if (price[0] != '$'):
                price = 'unknown'

        # print data to terminal for now
        print(count, end=' ')
        print('{PRICE: ' + price + '}', end=' ')
        print('{TITLE: ' + title + '}')
        count = count + 1

        # wait until the 'next' button is visible
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))
        # go to next city
        except:
            break
        # move to 'next' button
        ActionChains(driver).move_to_element(driver.find_element(
            By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]'))

        # wait until 'next' button is clickable
        ele = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))

        # click on element
        prev_link = cur_link
        # time.sleep(5)
        driver.execute_script("arguments[0].click();", ele)
        cur_link = driver.current_url
