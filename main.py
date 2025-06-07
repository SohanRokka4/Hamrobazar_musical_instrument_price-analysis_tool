from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import csv


def main():
    hamrobazar_scrapper()


def hamrobazar_scrapper():
    
# Configure Firefox with headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')  # Important for some sites

# Initialize WebDriver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        url = "https://hamrobazaar.com/category/instrument-guitars/4326E6AE-BBB1-4C91-984E-55FAB6A08864/7F0EC5AD-1F13-4BFD-83F1-8EDF7FD9CE4F"
        driver.get(url)
    
    # Wait for initial content and scroll to load all listings
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-title")))
    
    # Scroll to bottom to trigger lazy loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    # Additional wait after scrolling
        time.sleep(3)
    
    # Parse the fully loaded page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Updated selectors - HamroBazaar often uses these classes
        listings = soup.find_all('div', class_='card-product-linear-info') or \
                soup.find_all('div', class_='listing-item') or \
                soup.find_all('div', class_='item--3jzY0')
    
        scraped_data = []
        for listing in listings:
            try:
                name = listing.find(class_=lambda x: x and 'title' in x).get_text(strip=True)
                price = listing.find(class_=lambda x: x and 'price' in x).get_text(strip=True)
                condition = listing.find(class_=lambda x: x and 'condition' in x).get_text(strip=True)
                location = listing.find(class_=lambda x: x and 'location' in x).get_text(strip=True)
                seller = listing.find(class_=lambda x: x and 'username' in x and 'fullname' in x).get_text(strip=True)
                listing_no = listing.find(class_=lambda x: x and 'username' in x and 'listing' in x).get_text(strip=True)
            
                scraped_data.append({
                    'name': name,
                    'price': price,
                    'condition': condition,
                    'location': location,
                    'seller': seller,
                    'listing_no': listing_no
                })
            except Exception as e:
                print(f"Error parsing listing: {str(e)}")
                continue
    
    # Save results
        with open('hamrobazaar_guitars.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=scraped_data[0].keys() if scraped_data else [])
            writer.writeheader()
            writer.writerows(scraped_data)
    
        print(f"Successfully scraped {len(scraped_data)} listings")
        print("Sample data:", scraped_data[:2] if scraped_data else "No data")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        with open('error_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()