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
count = 0

for c in Tcities:
    curl = 'https://' + c + '.craigslist.org'
    b = False
    driver.get(curl)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'auto parts')))
    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    time.sleep(2)
    element.click()

    time.sleep(5)

    prev_link = ""
    cur_link = driver.current_url

    # simple solution to check whether the next page arrow is working,
    # after clicking the button, if the link doesn't change, go to next city
    while (cur_link != prev_link):
        if (b):
            break
        # row, skips last row?
        for i in range(1, 25):
            if (b):
                break
            # column
            for k in range(1, 6):
                time.sleep(1)
                # find the element on the webpage
                x = driver.find_elements(
                    By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[%s]/li[%s]/div/a' % (k, i))
                time.sleep(1)

                # case for a page that isn't full, want it to leave asap
                if (x == []):
                    b = True
                    break
                # otherwise extract the only element
                else:
                    e = x[0]

                # wait until next element is visible
                WebDriverWait(driver, 1).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[%s]/li[%s]/div/a' % (k, i))))

                # move to next element
                ActionChains(driver).move_to_element(driver.find_element(
                    By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[%s]/li[%s]/div/a' % (k, i)))

                # wait until element is clickable
                ele = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[%s]/li[%s]/div/a' % (k, i))))

                # click on element
                driver.execute_script("arguments[0].click();", ele)

                # make sure item exists before clicking
                time.sleep(5)
                driver.back()
                time.sleep(5)
                print(count)
                count = count + 1

        # move to arrow
        ActionChains(driver).move_to_element(driver.find_element(
            By.XPATH, '//*[@id="search-toolbars-1"]/div[2]/button[3]'))

        # wait until forward arrow is visible, then find it
        arrow = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="search-toolbars-1"]/div[2]/button[3]')))

        # set previous link and go to the next page
        prev_link = cur_link
        driver.execute_script("arguments[0].click();", arrow)
        time.sleep(8)
        cur_link = driver.current_url

    time.sleep(5)
