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

    a = 1 # anchor counter

    print ("In "+ c + " right now!")

    
    curl= "https://offerup.com/explore/sck/tx/" + c + "/5/9"
    driver.get(curl)
    time.sleep(1)
    
    genericPath = '//*[@id="__next"]/div[5]/div[2]/div[3]/main/div[3]/div/div[1]/div/a['

    
    time.sleep(1)

    while (True):
        item1 = genericPath + str(a) + "]"
        try:
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
                (By.XPATH, item1)))
        # go to next city
        except:
            last = True
            break
        
        #CLICK ON ITEM
        x = driver.find_element(By.XPATH, item1)
        element = driver.find_element(By.XPATH, item1)
        print ("ITERATION " + str(a))
        
        #PRINT NAME, PRICE, LOCATION
        print(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, item1))).get_attribute("aria-label"))
        element.click()
        time.sleep(1)
        
        #PRINTING DESCRIPTION
        descPath = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/p'
        descWithDetails = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div/p'
        print("Description: ")
        try:
            #Prints this if "Details exist"
            print(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, descWithDetails))).text)
        except:
            #Checking if "Description" exists
            try:
                #Prints Description
                print(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, descPath))).text)
            except:
                try:
                    #Prints this if Description has a scroll bar
                    descPath2 = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div[1]/div/div/div/p'
                    print((WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, descPath2))).text))
                except:
                    print("No description")

        #GET PRODUCT ID
        url = driver.current_url
        parts = url.split("/")
        productID = parts[-1]
        print("Product ID: " + productID)

        print("\n ********* \n")
        time.sleep(1)
        a += 1 # increment anchor
        item1 = genericPath + str(a) + "]"
        driver.get(curl)
        


