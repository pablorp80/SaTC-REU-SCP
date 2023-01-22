import os
import time
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
Tcities = {'sanantonio', 'austin', 'houston', 'lubbock', 'dallas', 'waco'}
Rcities = {'detroit', 'chicago', 'stlouis',
           'memphis', 'baltimore', 'milwaukee'}

for c in Tcities:
    curl = 'https://' + c + '.craigslist.org'
    driver.get(curl)
    link = driver.find_element_by_link_text('auto parts')
    link.click()
    time.sleep(4)
