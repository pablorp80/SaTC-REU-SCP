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

    e = driver.find_element(
        By.XPATH, '//*[@id="search-results-page-1"]/ol/ol/ol[1]/li[1]/div/a')

    html = e.get_attribute('innerText')
    print(html)
    time.sleep(5)
