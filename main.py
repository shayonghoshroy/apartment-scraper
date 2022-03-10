from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd
import requests
import time

def get_attributes(link):
    # go thru each link and populate csv file
    driver.get(link)

    # get name of apartment
    name = driver.find_element_by_id("propertyName").text
    print("Name:", name)

    # get google review
    search_name = name.replace(" ", "+")
    driver.get('https://www.google.com/search?q='+search_name+'+apartment+irving+texas')
    # if google review doesn't exist, get the apartments.com review
    try:
        review = driver.find_elements_by_xpath("//*[@class='Ob2kfd']")
        review = review[0].text.split("\n")[0]
        print("Google review:", review)
    except:
        try:
            review = driver.find_element_by_xpath('.//span[@class = "reviewRating"]').text
            print("Apartments.com review:", review)
        except:
            review = "NONE"
            print("review:", review)
    
    driver.get(link)
   

    # get address
    for elem in driver.find_elements_by_xpath("//*[@class='propertyAddressContainer']"):
        address = elem.text
    address = address.split("\n")
    neighborhood = address[1]
    address = address[0]
    print("Address:", address)
    print("Neighborhood:", neighborhood)

    # washer and dryer in unit
    washer_dryer = ('In Unit Washer & Dryer' in driver.page_source or 'Washer/Dryer' in driver.page_source)
    print("Washer/Dryer:", washer_dryer)

    # wifi
    wifi = ('Wi-Fi' in driver.page_source)
    print("Wi-Fi:", wifi)

    # AC
    ac_heating = ("Air Conditioning" in driver.page_source and "Heating" in driver.page_source)
    print("A/C and Heating:", ac_heating)

    # dishwasher
    dishwasher = ('Dishwasher' in driver.page_source)
    print("Dishwasher:", dishwasher)

    # disposal
    disposal = ('Disposal' in driver.page_source)
    print("Disposal:", disposal)

    # walk in closets
    walk_in = ("Walk-In Closets" in driver.page_source)
    print("Walk-In Closets:", walk_in)

    # balcony
    balcony = ("Balcony" in driver.page_source)
    print("Balcony:", balcony)
   
    # parking
    parking = ("Parking" in driver.page_source)
    print("Parking:", parking)

    # pets
    pets = ("Dogs Allowed" in driver.page_source)
    print("Pets Allowed:", pets)

    # pool
    pool = ("Pool" in driver.page_source)
    print("Pool:", pool)

    # fitness center
    fitness_center = ("Fitness Center" in driver.page_source)
    print("Fitness Center:", fitness_center)


    # expand all detail buttons
    for button in driver.find_elements_by_xpath("//*[@class='actionLinks expandSectionBtn js-modelExtension']"):
        # clicking on the button
        try:
            button.click()
        except:
            pass

    print()
    for elem in driver.find_elements_by_xpath("//*[contains(@class, 'pricingGridItem')]"):
        if ("2 bed" in elem.text and "2 bath" in elem.text) or ("2 beds" in elem.text and "2 baths" in elem.text):
            attributes = elem.text
            attributes = attributes.split("\n")
            floorplan_id = attributes[0]
            print("Floorplan ID:", floorplan_id)

           

            # price to sq ft ratio
            #price = attributes.index('price') + 1
            #price = attributes[price]
            #price = price[1:]
            price = elem.find_element_by_xpath('.//span[@class = "rentLabel"]').text
            price = price.split(" – ")
            price = price[0]
            price = price.replace("$", "")

            #square_feet = attributes.index('square feet') + 1
            #square_feet = attributes[square_feet]
            try:
                square_feet = elem.find_element_by_xpath('.//span[@class = "detailsTextWrapper"]').text
                square_feet = square_feet.split(", ")
                square_feet = square_feet[2]
                square_feet = square_feet.split(" – ")
                square_feet = square_feet[0]
                square_feet = square_feet.split(" ")
                square_feet = square_feet[0]
            except:
                square_feet = attributes.index('square feet') + 1
                square_feet = attributes[square_feet]
        
            price_per_sqft = int(price.replace(",", "")) / int(square_feet.replace(",", "")) 

            print("Price:", price)
            print("Square Feet:", square_feet)
            print("Price per Square Feet:", price_per_sqft)

            print("Other Attributes:")
            other_attributes = ''
            for attribute in attributes:
                other_attributes += attribute + ', '
            print(other_attributes)
            print()

            # RAW DUMP DF TO CSV
            dict = {'Name': name, 'Link': link, 'Address': address, 'Neighborhood': neighborhood, 'Price': price, 'Square Feet': square_feet, 
                'Price per Square Feet': price_per_sqft, 'Floor Plan ID': floorplan_id, 'Washer/Dryer': washer_dryer, 'Wi-Fi': wifi, 'A/C and Heating': ac_heating, 
                'Parking': parking, 'Google Review': review, 'Dishwasher': dishwasher, 'Disposal': disposal, 'Pets Allowed': pets, 'Pool': pool, 
                'Walk-In Closets': walk_in, 'Balcony': balcony, 'Fitness Center': fitness_center, 'All Attributes': other_attributes}
            return dict

            #TODO: ADD SCORE

            #TODO: FIGURE OUT WHY EACH APARTMENT ONLY HAS 1 FLOOR PLAN...

            """
            POSSIBLE NEIGHBORHOODS
            'Urban Center Irving', 'Grapevine', 'Hurst/Euless/Bedford', 'Valley Ranch', 
            'Las Colinas', 'Koreatown/Gribble', 'Farmers Branch', 'Coppell', 'Irving', 
            'Cypress Waters', 'Carrollton', 'Downtown Carrollton', 'Northwest Dallas', 
            'Original Town'
            """
            # neighborhood rankings
            # 1 Urban Center Living
            # 2 Las Colinas
            # 3 Valley Ranch

            #TODO: WRITE SCORE TO DF

# start timer
start = time.time()

# initialize the Chrome driver
option = webdriver.ChromeOptions()
#option.add_argument('headless')

driver = webdriver.Chrome(os.getcwd() + "/chromedriver", options=option)
driver.set_window_size(1024, 600)
driver.maximize_window()


url = 'https://www.apartments.com/apartments/min-2-bedrooms-2-bathrooms-under-3600/air-conditioning-washer-dryer-dishwasher-parking-walk-in-closets/?bb=sj3gm57xzJvp6rp7B&rt=4,5&mid=20220523'
driver.get(url)

# get total number of pages
for elem in driver.find_elements_by_xpath('.//span[@class = "pageRange"]'):
    total_pages = int(elem.text[-1])

links = []
# loop thru pages and collect links
for x in range(total_pages):
    if x != 0:
        next_page=driver.find_element_by_link_text(str(x+1))
        next_page.click()
        time.sleep(3)
    elems = driver.find_elements_by_class_name("property-link")
    links += [elem.get_attribute('href') for elem in elems]

# remove duplicates
links = [i for n, i in enumerate(links) if i not in links[:n]]
print(len(links), "links found...")

# dataframe
'''
column_names =  ['Link', 'Name', 'Address', 'Neighborhood', 'Price', 'Square Feet', 
    'Price per Square Feet', 'Floor Plan ID', 'Washer/Dryer', 'Wi-Fi', 'A/C and Heating', 
    'Parking', 'Google Review', 'Dishwasher', 'Disposal', 'Pets Allowed', 'Pool', 
    'Walk-In Closets', 'Balcony', 'Fitness Center', 'All Attributes']
    df = pd.DataFrame(columns = column_names)
'''
df = pd.DataFrame()

link = 'https://www.apartments.com/801-lasco-irving-tx/p42dr6r/'
get_attributes(link)

for link in links:
    dict = get_attributes(link)
    df = df.append(dict, ignore_index = True)

    


#TODO: SAVE DF AS CSV OR EXCEL FILE?
print(df)

# check that all links are in the df
for link in links:
    if link not in df.values:
        print('ERROR: THE FOLLOWING LINK IS NOT IN THE DF')
        print("link", link)

#TODO: MAUNALLY PLUG THIS DUDE's STATS IN: https://www.apartments.com/cortland-macarthur-irving-tx/k9n8jj9/

df.to_excel('raw-apartments.xlsx')


print("EXECUTION TIME:", (time.time())-start)

time.sleep(3)
driver.close()


