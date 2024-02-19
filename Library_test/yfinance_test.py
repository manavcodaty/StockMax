import yfinance as yf


# Download data for Apple Inc. for the year 2020
data = yf.download('nvda','2016-01-01','2024-2-4')
# Print the downloaded data
print(data)