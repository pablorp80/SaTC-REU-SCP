import time
from selenium import webdriver
from bs4 import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(ChromeDriverManager().install())

time.sleep(5)
# both lists subject to change, but must be the actual craigslist title
Tcities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas', 'waco'}
Rcities = {'detroit', 'chicago', 'stlouis',
           'memphis', 'baltimore', 'milwaukee'}

# number of items, just for testing purposes
count = 1

for c in Tcities:
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))
    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    time.sleep(5)
    element.click()

    time.sleep(10)

    x = driver.find_elements(By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[1]/li[1]/div/a')

    # case for a page that isn't full, want it to leave asap
    if (x == []):
        print('nothing found')
        # otherwise extract the only element
    else:
        e = x[0]

    e.click()

    prev_link = ""
    cur_link = driver.current_url

    # simple solution to check whether the next page arrow is working,
    # after clicking the button, if the link doesn't change, go to next city
    while (cur_link != prev_link):
        # row, skips last row?

        # wait until next element is visible
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))

        # move to next element
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]'))

        # wait until element is clickable
        ele = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/header/div[1]/div/a[3]')))

        # click on element
        prev_link = cur_link
        driver.execute_script("arguments[0].click();", ele)

        # make sure item exists before clicking
        time.sleep(1)
        print(count)
        count = count + 1
        cur_link = driver.current_url
