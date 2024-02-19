import sqlite3

import fire
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures


def create_database():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS stocks
                 (name TEXT PRIMARY KEY, price REAL)"""
    )
    sample_stocks = [("AAPL", 145.56), ("GOOGL", 1154.23), ("AMZN", 2942.45)]
    c.executemany("INSERT OR IGNORE INTO stocks VALUES (?, ?)", sample_stocks)
    conn.commit()
    conn.close()


def create_model():
    data = np.array([[1, 145.56], [2, 1154.23], [3, 2942.45]])
    X = data[:, 0].reshape(-1, 1)
    y = data[:, 1].reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    return model


def scrape_stock_info(symbol):
    url = f"https://www.google.com/search?q={symbol}+stock"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find("div", {"class": "IsqQVc-LgbsSe fxKbKc"}).text
        return float(price.replace(",", ""))
    except Exception:
        return None


def view_stock(symbol):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stocks WHERE name=?", (symbol,))
    stock = c.fetchone()
    conn.close()
    if stock:
        print(f"{symbol}: ${stock[1]}")
    else:
        print(f"No stock with symbol {symbol} found.")


def predict_stock(symbol):
    stock_price = scrape_stock_info(symbol)
    if stock_price is not None:
        X_new = np.array([[1]]).reshape(1, -1)
        y_pred = model.predict(X_new)
        print(f"Predicted price for {symbol}: ${y_pred[0]:.2f}")
    else:
        print(f"Could not find stock price for {symbol}.")


def train_model():
    data = np.array([[1, 145.56], [2, 1154.23], [3, 2942.45]])
    X = data[:, 0].reshape(-1, 1)
    y = data[:, 1].reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model_poly = LinearRegression()
    model_poly.fit(X_poly, y)
    y_pred = model_poly.predict(poly.fit_transform(X_new))
    print(f"Mean Squared Error: {mean_squared_error(y, model.predict(X))}")


if __name__ == "__main__":
    create_database()
    model = create_model()
    fire.Fire({"view": view_stock, "predict": predict_stock, "train": train_model})
