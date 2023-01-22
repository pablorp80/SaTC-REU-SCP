from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import *
from random import randrange
import wget
import os

driver = webdriver.Chrome(ChromeDriverManager().install())

#reads san antonio city is covered under houston
Tcities = {"houston", "dallas", "waco", "lubbock", "austin"}



for c in Tcities:
    # /5 - Vehicles
    # /9 - Autoparts and accessories
    curl= "https://offerup.com/explore/sck/tx/" + c + "/5/9"
    driver.get(curl)
    time.sleep(5)
    