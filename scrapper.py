from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os


def main():
    hamrobazar_scrapper()


def hamrobazar_scrapper():
    
# Configure Firefox with headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')  # Important for some sites

# Initialize WebDriver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    page_source = 'https://hamrobazaar.com/category/instrument-guitars/4326E6AE-BBB1-4C91-984E-55FAB6A08864/7F0EC5AD-1F13-4BFD-83F1-8EDF7FD9CE4F'

    url = "https://hamrobazaar.com/category/instrument-guitars/4326E6AE-BBB1-4C91-984E-55FAB6A08864/7F0EC5AD-1F13-4BFD-83F1-8EDF7FD9CE4F"
    driver.get(url)
    scraped_data = []
    repeat = 0
    count = 0
    seen_listings = set()
    seen_listings.clear()
    for _ in range(611): 
            # Wait for listings to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card-product-linear-info, .listing-item, .item--3jzY0")))

        new_listings = 0 #initalise new_listings as zero for every iteration of the scrool loop

            # Get all listing elements using Selenium (live DOM)
        listings = driver.find_elements(By.CSS_SELECTOR, ".card-product-linear-info, .listing-item, .item--3jzY0")


        for listing in listings:
            try:
                    # Extract key fields
                name = listing.find_element(By.CSS_SELECTOR, "[class*='title']").text
                price = listing.find_element(By.CSS_SELECTOR, "[class*='price']").text
                seller = listing.find_element(By.CSS_SELECTOR, "[class*='username-fullname']").text
                    
                    # Create unique identifier (combination of name, price and ad number)
                listing_id = f"{name}-{price}-{seller}"
                    
                if listing_id not in seen_listings:
                    new_listings +=1
                    seen_listings.add(listing_id)
                    condition = listing.find_element(By.CSS_SELECTOR, "[class*='condition']").text
                    location = listing.find_element(By.CSS_SELECTOR, "[class*='location']").text
                    ads_no = listing.find_element(By.CSS_SELECTOR, "[class*='username-listing']").text
                    listing_time = listing.find_element(By.CSS_SELECTOR, "[class*='time']").text
        
                    scraped_data.append({                            
                        'name': name,
                        'price': price,
                        'condition': condition,
                        'location': location,
                        'seller': seller,
                        'ads_no':ads_no,
                        'listing_time': listing_time
                    })
                
                    
            
                    
            except Exception as e:
                print(f"Error parsing listing {len(scraped_data)} in scroll no {_}: {str(e)}")
                continue
        if new_listings == 0:
            repeat +=1            
                           
        if len(listings) >= 2:
            driver.execute_script("window.scrollBy(0, 800);")
            count += 1
        listings = driver.find_elements(By.CSS_SELECTOR, ".card-product-linear-info, .listing-item") 
             # Wait for listings to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card-product-linear-info, .listing-item, .item--3jzY0")))
        time.sleep(5)
            # Stop if no new listings found after scroll
        if repeat >= 5:
            print("No new listings found, ending scrape.")
            break

            


    with open('hamrobazaar_guitars.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=scraped_data[0].keys() if scraped_data else [])
        writer.writeheader()
        writer.writerows(scraped_data)
    os.system('echo -e "\a"')#makes beep when scraping is done
    print(f"Successfully scraped {len(scraped_data)} listings")
    print(f"scrool count ={count} ")

    
        

if __name__ == "__main__":
    main()