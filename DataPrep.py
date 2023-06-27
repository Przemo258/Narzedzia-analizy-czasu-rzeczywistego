import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

STOCK_NAME = "AMD"
FILE_NAME = "data.csv"


def download_data():
    data = yf.download(STOCK_NAME)
    df = data['Close']
    df.to_csv(FILE_NAME)


def load_data():
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.asfreq('B')
    df.fillna(method='ffill', inplace=True)
    return df


def load_prepared_data(num_lags=5):
    df = load_data()

    for i in range(1, num_lags + 1):
        df[f"Close_{i}"] = df['Close'].shift(i)

    df = df.dropna()

    return df


if __name__ == "__main__":
    download_data()
    df = load_data()
    plt.figure(figsize=(10, 5))
    plt.plot(df)
    plt.title(STOCK_NAME)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.savefig(f"./plots/{STOCK_NAME}.png")
    plt.figure(figsize=(10, 5))
    plt.hist(df['Close'], bins=50)
    plt.title(f'{STOCK_NAME} Histogram')
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.savefig(f"./plots/{STOCK_NAME}_Histogram.png")
