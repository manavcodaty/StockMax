import pandas as pd

# Read the CSV file
df = pd.read_csv('stocks_portfolio.csv')

# Read a specific column
column = df['Symbol']

# Print the column
print(column)