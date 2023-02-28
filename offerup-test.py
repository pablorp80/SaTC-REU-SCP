#fixme : TO DO NOW:
# catch if there is no description at all. 
# something wrong with scroll descriptions. maybe make it the first test case.
# check out a scroll method

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
import datetime

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install())

#reads san antonio city is covered under houston
Tcities = {"houston", "dallas", "waco", "lubbock", "austin"}
CaliCities = {"san_francisco", "oakland", "east_los_angeles", "bakersfield", "san_jose", "san_diego", "sacramento"}
curlRoot = "https://offerup.com/explore/sck/ca/"

myDirectoryPath = "C:/Users/Misty Kurien/Documents/Baylor/Sophomore Spring/ResearchPosition/output"

for c in CaliCities:
    # /5 - Vehicles
    # /9 - Autoparts and accessories

    a = 1 # anchor counter

    print ("In "+ c + " right now!")

    
    curl= curlRoot + c + "/5/9"
    driver.get(curl)
    time.sleep(1)
    
    #this is the generic path of a an item on the main page
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
        #print(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, item1))).get_attribute("aria-label"))
        #element.click()
        #time.sleep(1)
        itemText = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, item1))).get_attribute("aria-label")
        
        
        element.click() 

        #PRINTING DESCRIPTION

        #path of description (basic case)
        descPath = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/p'
        #path of description when there is Details heading
        descWithDetails = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div/p'
        

        time.sleep(5)
        #GET PRODUCT ID
        url = driver.current_url
        parts = url.split("/")
        productID = parts[-1]
        print("Product ID: " + productID)

        print("Description: ")

        if ("Description" in driver.page_source):
            try :
                details_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Details')]")
            # Check if the "details" is displayed
                if details_element.is_displayed():
                    print("DETAILS BLOCK") #debugging
                    descriptionText = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descWithDetails))).text
                    print(descriptionText)
            except:
                #either going to be a description with "see more", or normal
                try:
                    #Prints this if Description has a "see more"
                    seeMore_element = driver.find_element(By.XPATH, "//*[contains(text(), 'See more')]")
                    time.sleep(1)
                    seeMore_element.click()
                    time.sleep(2)
                    print("IN SEE MORE")
                    #//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div/div/div/p/text()
                    descPath2 = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div/div/div/p/text()'

 
                    # Wait for the description element to become visible
                    description_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, descPath2)))
                    print(description_element)
                    # Retrieve the text of the description element
                   # description_text = description_element.text
                    #print(description_text)
                    
                except:
                    #Description without scroll (basic case)
                    descriptionText =WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descPath))).text
                    print(descriptionText)
                    
            
        else:
            descriptionText = "No description"
            print("No description")
        


        
        #GET USER NAME
        

        
        

        #DETAILS
       

        #TIME
        

        #IMAGES
       
    
        #FILE STUFF
       


        print("\n ********* \n")
        time.sleep(1)
        a += 1 # increment anchor
        item1 = genericPath + str(a) + "]"
        driver.get(curl)
        


