from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

url = "https://hamrobazaar.com/category/instrument-guitars/4326E6AE-BBB1-4C91-984E-55FAB6A08864/7F0EC5AD-1F13-4BFD-83F1-8EDF7FD9CE4F"

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in background
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to render
    
    # Option 1: Parse HTML directly
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    listings = soup.find_all('div', {'class': 'listing-item'})  # Update class based on actual page
    
    scraped_data = []
    for listing in listings:
        try:
            name = listing.find('h2', {'class': 'title'}).text.strip()
            price = listing.find('span', {'class': 'price'}).text.strip()
            condition = listing.find('span', {'class': 'condition'}).text.strip()
            negotiable = 'Negotiable' in listing.text  # Or look for specific element
            
            scraped_data.append({
                'name': name,
                'price': price,
                'condition': condition,
                'negotiable': negotiable
            })
        except Exception as e:
            print(f"Error parsing listing: {e}")
            continue
    
    # Option 2: Try to extract JSON data from script tags
    scripts = soup.find_all('script')
    for script in scripts:
        if 'window.__INITIAL_STATE__' in script.text:
            json_str = script.text.split('window.__INITIAL_STATE__ = ')[1].split(';')[0]
            data = json.loads(json_str)
            # Navigate through the JSON structure to find product data
            # This would be more reliable if available
    
    print(scraped_data)
    
finally:
    driver.quit()