import requests
from bs4 import BeautifulSoup
import csv
import time

def scrapper():
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"

    for page in range(1, 6):  # Scrape first 5 pages
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        books = soup.find_all('article', class_='product_pod')
    
        with open('books_all_pages.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text
                writer.writerow([title, price])
    
        print(f"Scraped page {page}")
        time.sleep(2)