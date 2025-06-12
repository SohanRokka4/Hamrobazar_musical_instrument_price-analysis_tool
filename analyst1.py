import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('clean_hamrobazaar_guitar.csv')

# Basic stats
print(df.describe(include='all'))  # Summary stats for numeric/categorical cols

# Price distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True)
plt.title('Price Distribution of Guitars')
plt.show()

# Top brands by count
df['brand'] = df['name'].str.extract(r'([A-Za-z]+)')  # Extract brands from names
brand_counts = df['brand'].value_counts().head(10)
brand_counts.plot(kind='bar', title='Top 10 Guitar Brands')