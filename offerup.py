from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import *
from random import randrange
import wget
import os

#now importing
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install())

#reads san antonio city is covered under houston
Tcities = {"houston", "dallas", "waco", "lubbock", "austin"}



for c in Tcities:
    # /5 - Vehicles
    # /9 - Autoparts and accessories
    curl= "https://offerup.com/explore/sck/tx/" + c + "/5/9"
    driver.get(curl)
    time.sleep(5)
    

#List<WebElement> allLinks = driver.findElements(By.tagName("a"))

    item1 = '//*[@id="__next"]/div[5]/div[2]/div[3]/main/div[3]/div/div[1]/div/a[1]'
# curl = "https://offerup.com/explore/sck/tx/houston/5/9"
    driver.get(curl)
    time.sleep(5)

    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, item1)))

    x = driver.find_element(By.XPATH, item1)

    element = driver.find_element(By.XPATH, item1)
    print(element.text) # it is reading the first object
    
    element.click()
    time.sleep(5)


