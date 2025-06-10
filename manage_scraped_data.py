import csv
from typing import List, Dict, Optional, Tuple, Set
import re


class data_cleaner:
    def __init__(self):
        self.file_path = 'hamrobazaar_guitars.csv'
        self.data = []
        self.headers = []
    
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


    def remove_duplicates(self) -> int:
        """
        Remove rows where all columns (except the specified ones) are identical.
    
        Args:
            none
    
        Returns:
            Number of duplicate rows removed.
        """

        unique_data = []
        seen = set()  # Track unique combinations
        duplicates_removed = 0
        for row in self.data:
    # Create a unique key from selected columns
            key = (row['name'], row['price'], row['condition'], row['seller'])
    
            if key not in seen:
                seen.add(key)
                unique_data.append(row)
            else:
                duplicates_removed += 1
        self.data = unique_data
        return duplicates_removed
    

    def clean_and_format_data(self) -> None:
        """
        Clean and standardize the data format according to the specified structure.
        Converts from original format to cleaned format.
        """
        cleaned_data = []
        
        for row in self.data:
            cleaned_row = {}
            
            # Clean name (remove extra spaces)
            cleaned_row['name'] = row['name'].strip()
            
            # Extract numeric price and convert to integer
            price_str = row['price']
            price_match = re.search(r'रू\.?\s*([\d,]+)', price_str)
            if price_match:
                cleaned_price = price_match.group(1).replace(',', '')
                cleaned_row['price'] = int(cleaned_price)
            else:
                cleaned_row['price'] = None
                
            # Clean condition (remove pipes and spaces)
            condition = row['condition'].replace('|', '').strip()
            cleaned_row['condition'] = condition if condition else None
            
            # Split location and time
            location_parts = row['location'].rsplit(' ', 3)  # Split from right
            if len(location_parts) >= 4 and location_parts[-2] == 'ago':
                cleaned_row['location'] = ' '.join(location_parts[:-2]).strip()
                cleaned_row['time'] = location_parts[-3] + ' ' + location_parts[-2]
            else:
                cleaned_row['location'] = row['location'].strip()
                cleaned_row['time'] = None
                
            # Clean seller name
            cleaned_row['seller'] = row['seller'].strip()
            
            # Extract number of ads posted by seller
            ad_match = re.search(r'(\d+)\s*Ad', row['listing_no'])
            cleaned_row['no_of_ad_posted_by_seller'] = int(ad_match.group(1)) if ad_match else None
            
            cleaned_data.append(cleaned_row)
        
        self.data = cleaned_data
        self.headers = list(cleaned_data[0].keys()) if cleaned_data else []

def main():
    editor = data_cleaner()
    editor.load_data()
    print(f"no of duplicates removed = {editor.remove_duplicates()}")
    editor.clean_and_format_data()
    editor.save_data()
        
if __name__ == "__main__":
    main()