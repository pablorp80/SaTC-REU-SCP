#TODO: will this work if the word "details" is in the description?

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
    
    genericPath = '//*[@id="__next"]/div[5]/div[2]/div[3]/main/div[3]/div/div[1]/div/a['

    #path of description (basic case)
    descPath = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/p'
    #path of description when there is Details heading
    descWithDetails = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div/p'
    descDetailsSeeMore = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div[1]/div/div/div/p'
    
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
                        time.sleep(1)
                        seeMore_element.click()
                        time.sleep(2)
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
                    time.sleep(1)
                    seeMore_element.click()
                    time.sleep(2)
                    print("IN SEE MORE")
                    #//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div/div/div/p/text()
                    descPath2 = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div/div/div/p'

 
                    # Wait for the description element to become visible
                    description_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, descPath2)))
                    descriptionText = description_element.text
                    print(descriptionText)
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
        """ descPath = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div/p'
        descWithDetails = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div/p'
        print("Description: ")
        try:
            #Prints this if "Details exist"
            descriptionText = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descWithDetails))).text
            print(descriptionText)
        except:
            #Checking if "Description" exists
            try:
                #Prints Description
                descriptionText =WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, descPath))).text
                print(descriptionText)
            except:
                try:
                    #Prints this if Description has a scroll bar
                    descPath2 = '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[2]/div/div[5]/div[2]/div[2]/div[1]/div/div/div/p'
                    descriptionText =(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, descPath2))).text)
                    print(descriptionText)
                except:
                    print("No description")
                    descriptionText = "No description" """

        
        #GET USER NAME
        try:
            username = driver.find_element(By.XPATH, '//*[@id="__next"]/div[5]/div[2]/main/div[1]/div/div[1]/div/div[5]/button/div/div[2]/p[1]').text
            print("Username: " + username)
        except: 
            print("Username: No username")

        """ #GET PRODUCT ID
        url = driver.current_url
        parts = url.split("/")
        productID = parts[-1]
        print("Product ID: " + productID) """
        

        #DETAILS
        '''parts = itemText.split("$")
        #name = parts[0].strip()
        #parts = parts[1].split("in")
        #price = parts[0].strip()
        region = parts[1].strip()'''
        name = itemText[0:itemText.rfind("$")]
        price = itemText[itemText.rfind("$") : itemText.rfind(" in")]
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
            websiteTime = element.text[0:(element.text.rindex("in"))]
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
            file = open(newdirectory + "/post.txt", "w", encoding='utf-8')
            file.write(name)
            file.close()

            file = open(newdirectory + "/date.txt", "w", encoding='utf-8')
            file.write(systemTime + "\n")
            file.write(websiteTime)
            file.close()

            file = open(newdirectory + "/username.txt", "w", encoding='utf-8')
            file.write(username)
            file.close()

            file = open(newdirectory + "/region.txt", "w", encoding='utf-8')
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
        time.sleep(1)
        a += 1 # increment anchor
        item1 = genericPath + str(a) + "]"
        driver.get(curl)
        


