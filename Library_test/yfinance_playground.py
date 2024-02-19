import pandas as pd
import yfinance as yf

tickers_list = ["aapl", "goog", "amzn", "BAC", "BA"] # example list
tickers_data= {} # empty dictionary

for ticker in tickers_list:
    ticker_object = yf.Ticker(ticker)

    #convert info() output from dictionary to dataframe
    temp = pd.DataFrame.from_dict(ticker_object.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    
    # add (ticker, dataframe) to main dictionary
    tickers_data[ticker] = temp


combined_data = pd.concat(tickers_data)
combined_data = combined_data.reset_index()
del combined_data["level_1"] # clean up unnecessary column
combined_data.columns = ["Ticker", "Attribute", "Recent"] # update column names

print(combined_data)

