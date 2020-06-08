#id
#company name
#industry
#sector
#stage
#state
#website
#team info
#address
#contact info
#notes

import time
import csv
import json
import pandas as pd
from selenium import webdriver




links = ["https://www.startupindia.gov.in/content/sih/en/search.html?industries=sih:industry/textilesandapparel&stages=Prototype%20Validation&roles=Startup&page=82"]


for i,link in enumerate(links):
    print(f'page {i+1} : {link}')

    driver = webdriver.Chrome('/usr/bin/chromedriver')

    try:
        driver.get(link)
        time.sleep(5)

        try:
            cards = driver.find_elements_by_class_name("category-card")
            print(len(cards))
            cardlinks = []

            k=0

            for card in cards:
                a = card.find_element_by_tag_name("a").get_attribute("href")
                cardlinks.append(a)
        except Exception as e:
            print(e)
            cardlinks=[]
            print("didn't find info")

        try:
            with open(f"textile2.csv","a") as f:
                writer = csv.writer(f)
                for cl in cardlinks:
                    writer.writerow([cl])
        except:
            print("error while saving links")

    except Exception as e:
        print(e)
        print("error!")

    driver.close()
