import yfinance as yf
import pandas as pd


def load_data(tickers, period="24mo", interval="1d"):
    data = yf.download(
        tickers,
        period=period,
        interval=interval,
        auto_adjust=True
    )["Close"]

    data = data.dropna(axis=1, how="all")
    return data
