import os
import time
from selenium import webdriver
from bs4 import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

# both lists subject to change, but must be the actual craigslist title
Tcities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas', 'waco'}
Rcities = {'detroit', 'chicago', 'stlouis',
           'memphis', 'baltimore', 'milwaukee'}

for c in Tcities:
    curl = 'https://' + c + '.craigslist.org'

    driver.get(curl)
    element = driver.find_element(By.LINK_TEXT, 'auto parts')
    element.click()

    time.sleep(10)

    # row
    for i in range(1, 25):
        # column
        for k in range(1, 6):
            e = driver.find_element(
                By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[%s]/li[%s]/div/a' % (k, i))
            e.click()
            time.sleep(5)
            driver.back()
            time.sleep(5)

    e.click()
    time.sleep(5)
