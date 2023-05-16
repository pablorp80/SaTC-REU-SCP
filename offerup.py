#fixme : TO DO NOW:
# willl this work if the word "details" is in the description?

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import *
from random import randrange
import wget
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import datetime
from os import chdir
import random
from itertools import cycle


service = Service(ChromeDriverManager().install())

# Create ChromeOptions object
options = webdriver.ChromeOptions()

# Create a WebDriver instance
driver = webdriver.Chrome(service=service, options=options)


#the basic URL for offerup
bigCitiesRoot = "https://offerup.com/explore/sck/"
#50 cities

bigCities = {"ny/new_york", "ca/los_angeles", "il/chicago", "tx/houston", "pa/philadelphia",
             "az/phoenix", "tx/san_antonio", "ca/san_diego", "tx/dallas", "ca/san_jose", 
             "tx/austin", "fl/jacksonville", "ca/san_francisco", "in/indianapolis", "oh/columbus",
             "tx/fort_worth", "nc/charlotte", "wa/seattle", "co/denver", "tx/el_paso", "mi/detroit", 
             "ma/boston", "tn/memphis", "tn/nashville", "or/portland", "ok/oklahoma_city",
             "nv/las_vegas", "md/baltimore", "ky/louisville", "wi/milwaukee", "nm/albuquerque",
             "az/tucson", "ca/fresno", "ca/sacramento", "mo/kansas_city", "ca/long_beach",
             "az/mesa", "ga/atlanta", "co/colorado_springs", "va/virginia_beach", "nc/raleigh",
             "ne/omaha", "fl/miami", "ca/oakland", "mn/minneapolis", "ok/tulsa",
              "ks/wichita", "la/new_orleans", "tx/arlington"}

#getting current directory
myDirectoryPath = os.path.dirname(os.path.abspath(__file__))
myDirectoryPath = myDirectoryPath + "/output"

#makes a new output folder if it doesn't exist
if (not os.path.isdir(myDirectoryPath)):
    os.mkdir(myDirectoryPath)

chdir(myDirectoryPath)

#cycles infinitely
for c in cycle(bigCities):
    

    a = 1 # anchor counter

    print ("In "+ c + " right now!")

    # /5 - Vehicles
    # /9 - Autoparts and accessories
    curl = bigCitiesRoot + c + "/5/9"
    #curl= curlRoot + c + "/5/9"
    driver.get(curl)
    time.sleep(random.uniform(1, 5))
    
    genericPath = '//*[@id="__next"]/div[5]/div[2]/div[3]/main/div[3]/div/div[1]/div/a['

    #path of description (basic case)
    descPath = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/p'
    #path of description when there is Details heading
    descWithDetails = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div/p'
    descDetailsSeeMore = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div[1]/div/div/div/p'
    
    time.sleep(random.uniform(1, 5))

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
        itemText = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, item1))).get_attribute("aria-label")
        href =  WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, item1))).get_attribute("href")
        href = href[href.find('/detail/')+len('/detail/'):href.find('?cid')]
        print(href) #this is the link listed on the offerup home page

        if (os.path.exists(myDirectoryPath+"/"+href)):
                print("folder already exists. going to next one")
                a += 1 # increment anchor
                item1 = genericPath + str(a) + "]"
                driver.get(curl)
                continue
        
        
        element.click() 

        #PRINTING DESCRIPTION

        time.sleep(5)

        #GET PRODUCT ID
        url = driver.current_url
        parts = url.split("/")
        productID = parts[-1]
        print("Product ID: " + productID)

        if ("Description" in driver.page_source):
            try :
                details_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Details')]")
            # Check if the "details" is displayed
                if details_element.is_displayed():
                    print("DETAILS BLOCK") #debugging
                    try:
                        #Details has a "See More" description
                        seeMore_element = driver.find_element(By.XPATH, "//*[contains(text(), 'See more')]")
                        time.sleep(random.uniform(1, 5))
                        seeMore_element.click()
                        time.sleep(random.uniform(2, 5))
                        print("IN SEE MORE - DETAILS")
                        description_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, descDetailsSeeMore)))
                        descriptionText = description_element.text
                        print(descriptionText)
                    except:
                        #Normal Description
                        descriptionText = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descWithDetails))).text
                        
                        print(descriptionText)
            except:
                #either going to be a description with "see more", or normal
                try:
                    #Prints this if Description has a "see more"
                    seeMore_element = driver.find_element(By.XPATH, "//*[contains(text(), 'See more')]")
                    time.sleep(random.uniform(1, 5))
                    seeMore_element.click()
                    time.sleep(random.uniform(2, 5))
                    print("IN SEE MORE")
                    descPath2 = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div/div/div/p'

 
                    # Wait for the description element to become visible
                    description_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, descPath2)))
                    descriptionText = description_element.text
                    print(descriptionText)
                    
                except:
                    #Description without scroll (basic case)
                    descriptionText =WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descPath))).text
                    print(descriptionText)
                    
            
        else:
            descriptionText = "No description"
            print("No description")
        
        #GET USER NAME
        try:
            username = driver.find_element(
                By.XPATH, 
                '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[1]/div/div[5]/button/div/div[2]/p[1]'
                ).text
            
            print("Username: " + username)

        except: 
            print("Username: No username")

    
        

        #DETAILS
        name = itemText[0:itemText.rfind("$")]
        price = itemText[itemText.rfind("$") : itemText.rfind(" in")]
        price = price.replace(',', '')
        price = price.replace('$', '')
        region = itemText[itemText.find(" in") + 4 : ]

        print("Item name: " + name)
        print("Item price: " + price)
        print("Region: " +  region)

        #TIME
        systemTime = str(datetime.datetime.now())
        print("System time: " + str(datetime.datetime.now()))
    
        xpath = "//*[contains(text(), 'ago')]"
        element = driver.find_element(By.XPATH, xpath)

        if element:
            websiteTime = element.text[0:(element.text.rindex(" in "))]
            print("Website time: " + websiteTime)
        else:
            print("Text containing the word 'ago' not found")

        #IMAGES
        images = driver.find_elements(By.XPATH, '//img')
        image_urls = [image.get_attribute("src") for image in images]
        def required_images(imageList):
            imageList = imageList[1:]
            imageList = [s for s in imageList if s.startswith('https://images.offerup.com/')]
            if (len(imageList) != 1):
                newSize = int(len(imageList)/2)
                imageList = imageList[0: newSize]
            return imageList

        image_urls = required_images(image_urls)
        i = 0
        for img in image_urls:
            i +=1
            print(str(i) + ". " + img )
    
        #FILE STUFF
        try:
            newdirectory = myDirectoryPath + "/" + productID[0:productID.find("?")]
            os.makedirs(newdirectory)
            file = open(newdirectory + "/title.txt", "w", encoding='utf-8')
            file.write(name)
            file.close()

            file = open(newdirectory + "/date.txt", "w", encoding='utf-8')
            file.write(systemTime + "\n")
            file.write(websiteTime)
            file.close()

            file = open(newdirectory + "/username.txt", "w", encoding='utf-8')
            file.write(username)
            file.close()

            file = open(newdirectory + "/city.txt", "w", encoding='utf-8')
            file.write(region)
            file.close()

            file = open(newdirectory + "/description.txt", "w", encoding='utf-8')
            file.write(descriptionText)
            file.close()

            file = open(newdirectory + "/price.txt", "w", encoding='utf-8')
            file.write(price)
            file.close()

            file = open(newdirectory + "/images.txt", "w", encoding='utf-8')
            for img in image_urls:
                file.write(img + "\n" )
            file.close()

            
        except:
            print("not possible to make folder")


        print("\n ********* \n")
        time.sleep(random.uniform(1, 5))
        a += 1 # increment anchor
        item1 = genericPath + str(a) + "]"
        driver.get(curl)
        

