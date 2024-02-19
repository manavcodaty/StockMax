import sqlite3
import sys

import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def create_database():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS stocks
                 (symbol TEXT PRIMARY KEY, price REAL)"""
    )
    conn.commit()
    conn.close()


def create_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def scrape_additional_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    symbol = soup.find("span", {"class": "symbol"}).text
    price = float(soup.find("span", {"class": "price"}).text.strip("$"))
    return {"symbol": symbol, "price": price}


def view_stock(symbol):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT price FROM stocks WHERE symbol=?", (symbol,))
    result = c.fetchone()
    conn.close()
    if result:
        print(f"Stock price for {symbol}: ${result[0]}")
    else:
        print(f"No stock found for {symbol}")


def predict_stock_price(model, symbol):
    try:
        # Fetch the current price from an API or another source
        current_price = ...
        # Preprocess the current price as required by your model
        X_new = np.array(current_price).reshape(1, -1)
        predicted_price = model.predict(X_new)
        print(f"Predicted price for {symbol}: ${predicted_price[0]:.2f}")
    except Exception as e:
        print(f"Error predicting stock price: {e}")


def add_stock_from_web(model):
    try:
        # Scrape the stock symbol and price from a web source
        url = "https://example.com/stock_source"
        stock_data = scrape_additional_info(url)

        # Add the stock to the database
        conn = sqlite3.connect("stocks.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO stocks (symbol, price) VALUES (?, ?)",
            (stock_data["symbol"], stock_data["price"]),
        )
        conn.commit()
        conn.close()

        # Train the model with the new stock data
        X = np.array([stock_data["price"]]).reshape(-1, 1)
        y = np.array([stock_data["price"]]).reshape(-1, 1)
        model = create_model(X, y)
        return model
    except Exception as e:
        print(f"Error adding stock from web: {e}")


def run_application():
    model = create_model(X, y)
    while True:
        try:
            main_menu()
            choice = int(input("Enter your choice: "))
            if choice == 1:
                symbol = input("Enter the stock symbol: ").upper()
                view_stock(symbol)
            elif choice == 2:
                symbol = input("Enter the stock symbol: ").upper()
                predict_stock_price(model, symbol)
            elif choice == 3:
                model = add_stock_from_web(model)
            elif choice == 4:
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")


def main_menu():
    print("Stock Application")
    print("1. View stock")
    print("2. Predict stock price")
    print("3. Add stock from web")
    print("4. Exit")


if __name__ == "__main__":
    create_database()
    X = ...
    y = ...
    run_application()
