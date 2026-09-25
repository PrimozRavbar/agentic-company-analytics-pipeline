import pandas as pd


def compute_features(prices):
    returns = prices.pct_change()

    features = {}

    # rolling volatility (10-day)
    features["volatility"] = returns.rolling(10).std()

    # momentum (10-day return)
    features["momentum"] = prices.pct_change(10)

    # rolling z-score of returns
    features["zscore"] = (
        (returns - returns.rolling(10).mean())
        / returns.rolling(10).std()
    )

    return features


def build_matrix(features_dict):
    df_list = []

    for name, df in features_dict.items():
        stacked = df.stack().reset_index()
        stacked.columns = ["date", "ticker", name]
        df_list.append(stacked)

    out = df_list[0]

    for df in df_list[1:]:
        out = out.merge(df, on=["date", "ticker"])

    return out
