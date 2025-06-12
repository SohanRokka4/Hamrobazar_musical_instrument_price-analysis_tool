import csv
from typing import List, Dict, Optional, Tuple, Set
import re


class data_cleaner:
    def __init__(self):
        self.file_path = 'hamrobazaar_guitars.csv'
        self.data = []
        self.headers = []
        self.cleaned_data = []
    
    def load_data(self) -> None:
        """Load data from the CSV file into memory."""
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            self.headers = reader.fieldnames
            self.data = [row for row in reader]
            
    def save_data(self) -> None:
        """Save the modified data back to the CSV file."""
        with open('clean_hamrobazaar_guitar.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)

    def delete_row(self, row_index: int) -> None:
        """Delete a row from the CSV data.
        
        Args:
            row_index: Index of the row to delete (0-based).
        """
        if row_index < 0 or row_index >= len(self.data):
            raise IndexError("Row index out of range")
            
        del self.data[row_index]


    

    def clean_and_format_data(self) -> None:
        """
        Clean and standardize the data format according to the specified structure.
        Converts from original format to cleaned format.
        """
        
        for row in self.data:
            cleaned_row = {}
            
            # Clean name (remove extra spaces)
            cleaned_row['name'] = row['name'].strip()
            
            # Extract numeric price and convert to integer
            price_str = row['price']
            price_match = price_str.split("रू.")[1].split("|")[0]
            cleaned_price = price_match.replace(",","").strip()
            cleaned_row['price'] = int(cleaned_price)

                
            # Clean condition (remove pipes and spaces)
            condition = row['condition'].replace('|', '').strip()
            cleaned_row['condition'] = condition if condition else None
            
            # Split location and time
            cleaned_row['location'] = row['location'].split('\n')[0].strip()
                
                
            # Clean seller name
            cleaned_row['seller'] = row['seller'].strip()
            
            # Extract number of ads posted by seller
            ads_no = row['ads_no'].replace('|',' ').strip().split(' ')
            cleaned_row['ads_no'] = int(ads_no[0])

            #extract the time seller posted the aad
            time = row['listing_time'].split(" ")
            if time[1] == 'mins':
                cleaned_row['listing_time_hrs'] = 1
            if time[1] == 'hours':
                cleaned_row['listing_time_hrs'] = (int(time[0])*1)
            if time[1] == 'days':
                cleaned_row['listing_time_hrs'] = (int(time[0])*24)
            if time[1] == 'months':
                cleaned_row['listing_time_hrs'] = (int(time[0])*720)
            if time[1] == 'years':
                cleaned_row['listing_time_hrs'] = (int(time[0])*8640)

            
        # ... adding categorizations
            cleaned_row['brand_tier'] = self.categorize_brand_tier(cleaned_row['name'],int(cleaned_price))
            cleaned_row['guitar_type'] = self.categorize_guitar_type(cleaned_row['name'])



            
            self.cleaned_data.append(cleaned_row)
        
        self.data = self.cleaned_data
        self.headers = list(self.cleaned_data[0].keys()) if self.cleaned_data else []
    


    

    def categorize_brand_tier(self,name,price):
        """Classify brands into premium, mid-range, or budget tiers"""

        brand_name = name.split(" ")
        dirt_cheap = ['givson', 'frender', 'epephone', 'clapton', 'mars', 'pluto', 'vt', 'venus', 'indian', 'hovner', 'signature', 'kasper', 'volume']
        budget = [ 'f6000', 'mantra', 'dreammaker', 'devisor', 'manaslu', '4-band', 'equaliser', 'tuner', 'dream', 'rocket']
        midrange = ['yamaha', 'ibanez', 'takamine', 'crafter', 'enya', 'jet', 'hex', 'cort', 'samick', 'sqoe', 'bacchus', 'cate', 'sx', 'k-marth', 'tagima']
        premium = ['gibson', 'fender', 'martin', 'taylor', 'prs', 'emg', 'gretsch']

        
        for brand in brand_name:
            if (brand.lower()  in premium and price < 50000) or (brand.lower()  in midrange and price < 18000):
                return 'bootleg/budget'
            elif brand.lower() in dirt_cheap:
                return 'indian_budget'
            elif brand.lower() in budget:
                return 'budget'
            elif brand.lower() in midrange:
                return 'midrange'
            elif brand.lower() in premium:
                return 'premium'
        return 'unknown'
    

    def categorize_guitar_type(self,title):
        terms = title.lower().split(" ")
        if 'ukulele' in terms or 'ukelele' in terms:
            return 'ukulele'
        elif 'bass' in terms:
            return 'bass'
        elif 'classical' in terms:
            return 'classical'
        elif 'nylon' in terms:
            return 'classical'
        elif ('electric' in terms and 'acoustic' not in terms) or ('electric' in terms and 'accoustic' not in terms):
            return 'electric'
        elif 'accoustic' in terms or 'acoustic' in terms:
            return 'acoustic'
        elif any(e in terms for e in ['stratocastor','les', 'paul', 'sg', 'strat', 'leapsul', 'teli', 'telicastor']):
            return 'electric'
        elif any(e in terms for e in ['accoustic','acoustic','4-band', 'equaliser', 'tuner','givson', 'frender', 'epephone', 'clapton', 'mars', 'pluto', 'vt', 'venus', 'indian', 'hovner', 'signature', 'kasper', 'volume']):
            return 'acoustic'
        else:
            return 'unknown'


    def remove_duplicates(self):
        seen = set()
        unique_data = []
        duplicates_removed = 0
    
        for row in self.data:
        # Create a tuple of the values from key columns
            row_key = tuple(str(row[col]) for col in ['name', 'price', 'seller', 'listing_time_hrs'])
        
            if row_key not in seen:
                seen.add(row_key)
                unique_data.append(row)
            else:
                duplicates_removed += 1
    
        self.data = unique_data
        return duplicates_removed  
        
    

    



def main():
    editor = data_cleaner()
    editor.load_data()
    editor.clean_and_format_data()
    print(f"no of duplicates removed = {editor.remove_duplicates()}")
    editor.save_data()
if __name__ == "__main__":
    main()