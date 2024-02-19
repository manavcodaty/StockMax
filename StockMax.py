#StockMax software
#This software is a stock portfolio management system that allows users to add, remove, view, update and predict stock prices.
#Made by: Manav Prasad Codaty
#MIT License

import yfinance as yf
import pandas as pd
from pandas import DataFrame
import time
from numerize import numerize 
import datetime
import plotly.graph_objects as go
import sys
from beibo import oracle
import numpy as np
import os
from nltk.sentiment import SentimentIntensityAnalyzer





        

def add_stock():
    print("----------Add a new stock----------")
    num_stocks = int(input("Enter the number of stocks you want to add: "))
    for i in range(num_stocks):
        symbol = input("Enter the stock symbol: ")
        buy_price = float(input("Enter the buy price: "))
        current_price = yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
        current_price = round(current_price, 2)
        ajd_close = yf.Ticker(symbol).history(period="1d")["Adj Close"].iloc[-1]
        symbol_high = yf.Ticker(symbol).info['dayHigh']
        symbol_low = yf.Ticker(symbol).info['dayLow']
        Market_cap = yf.Ticker(symbol).info['marketCap']
        Market_cap = numerize.numerize(Market_cap)
        week_high = yf.Ticker(symbol).info['fiftyTwoWeekHigh']
        week_low = yf.Ticker(symbol).info['fiftyTwoWeekLow']
        dict = {
            'Symbol': [symbol],
            
            'Buy Price': [buy_price], 
            
            'Current Price': [current_price],
            
            'Adjacent Close': [ajd_close],
            
            'Day High': [symbol_high],
            
            'Day Low': [symbol_low],
            
            'Market Cap': [Market_cap],
            
            '52 Week High': [week_high],
            
            '52 Week Low': [week_low]
            
            }
        df = pd.DataFrame(dict)
        df.to_csv('stocks_portfolio.csv', mode='a', index=False, header=False)
        print("Stock added successfully.")
        
    time.sleep(0.5)
    main_menu()
        
        
        
def remove_stock():
    print("----------Remove a stock----------")
    symbol = input("Enter the stock symbol: ")
    df = pd.read_csv('stocks_portfolio.csv')
    df = df[df['Symbol'] != symbol]
    df.to_csv('stocks_portfolio.csv', index=False)
    print("Stock removed successfully.")
    
    
def view_all_stocks():
    print("----------View all stocks----------")
    df = pd.read_csv('stocks_portfolio.csv')
    print(df.to_string())
    
    
def view_stock():
    print("----------View a stock----------")
    symbol = input("Enter the stock symbol: ")
    df = pd.read_csv('stocks_portfolio.csv')
    print(df[df['Symbol'] == symbol.upper()].to_string(index=False))
    print("1. View stock chart")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        view_stock_chart(symbol)
    elif choice == "2":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
    def view_stock_chart(symbol):
        df = yf.download(symbol, period="max", interval="1d")
        fig = go.Figure(data=go.Scatter(x=df.index,y=df['Close'], mode='lines'))
        fig.update_layout(title={'text': symbol.upper(), 'x':0.5})
        fig.show()

    
    
    
def update_stock():
    print("----------Update a stock----------")
    symbol = input("Enter the stock symbol: ")
    buy_price = float(input("Enter the new buy price: "))
    df = pd.read_csv('stocks_portfolio.csv')
    df.loc[df['Symbol'] == symbol, 'Buy Price'] = buy_price
    df.to_csv('stocks_portfolio.csv', index=False)
    print("Stock updated successfully.")
    
    
    
    
    


def predict_stock_price():
    print("----------Predict stock price----------")
    print("1. Single stock prediction")
    print("2. Multiple stock prediction")
    print("3. Portfolio prediction")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        symbol = input("Enter stock symbol: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        num_days = int(input("Enter number of days to predict: "))
        symbol.upper()
        oracle(
        portfolio = [symbol], #stocks you want to predict
        start_date = start_date, #date from which it will take data to predict
        prediction_days = num_days #number of days you want to predict
        )
        time.sleep(0.5)
        main_menu()
    elif choice == "2":
        print("Enter number of symbols you want to predict: ")
        num_symbols = int(input())
        symbols = []
        for i in range(num_symbols):
            symbol = input("Enter stock symbol: ")
            symbols.append(symbol)
        start_date = input("Enter start date (YYYY-MM-DD): ")
        num_days = int(input("Enter number of days to predict: "))
        oracle(
        portfolio = symbols, #stocks you want to predict
        start_date = start_date, #date from which it will take data to predict
        prediction_days = num_days #number of days you want to predict
        )
        time.sleep(0.5)
        main_menu()
    elif choice == "3":
        df = pd.read_csv('stocks_portfolio.csv')
        symbols = df['Symbol'].tolist()
        print("Symbols successfully loaded.")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        num_days = int(input("Enter number of days to predict: "))  
        oracle(
        portfolio = symbols, #stocks you want to predict
        start_date = start_date, #date from which it will take data to predict
        prediction_days = num_days #number of days you want to predict
        )
        
    elif choice == "4":
        time.sleep(0.5)
        main_menu()
    else:
        print("Invalid choice. Please try again.")
    

    


    
        
    
    
def open_chatbot():
    print("----------Chatbot----------")
    print("Opening chatbot......")
    os.system('streamlit run chatbot.py')
    

    
def ai_menu():
    print("----------Ai----------")
    print("1. Predict stock price")
    print("2. Chatbot")
    print("3. Exit")
    print("4. Exit programme")
    choice = input("Enter your choice: ")
    if choice == "1":
        predict_stock_price()
    elif choice == "2":
        open_chatbot()
    elif choice == "3":
        main_menu()
    elif choice == "4":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        



def main_menu():
    print("----------Stock Application----------")
    print("1. Add a new stock")
    print("2. Remove a stock")
    print("3. View all stocks")
    print("4. View a stock")
    print("5. Update a stock")
    print("6. Use Ai")
    print("7. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        add_stock()
    elif choice == "2":
        remove_stock()
    elif choice == "3":
        view_all_stocks()
    elif choice == "4":
        view_stock()
    elif choice == "5":
        update_stock()
    elif choice == "6":
        ai_menu()
    elif choice == "7":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        main_menu()

    

main_menu()