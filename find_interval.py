import numpy as np
import pandas as pd


def simulate_stock_price(S0, mu, sigma, T=1, N=500):
    dt = T/N  # time step
    dW = np.sqrt(dt) * np.random.randn(N)  # increments of Wiener process
    W = np.cumsum(dW)  # standard Brownian motion

    # Calculating stock price at each time step
    t = np.linspace(0, T, N)
    stock_price = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)
    
    return t, stock_price

def interval(file):
    data = pd.read_csv(file,names=['time', 'complete', 'o', 'h', 'l', 'Close', 'v'])
    #data["Close"] = (data["Bid"] + data["Ask"])/2
    log_returns = np.log(data["Close"]/data["Close"].shift(1))
    data["log returns"] = log_returns[1:]

    sigma = np.sqrt(np.var(data["log returns"]))
    mu = np.mean(data["log returns"]) + sigma**2/2
    S0 = data["Close"].iloc[-1]

    final_prices = []
    for i in range(10000):
        t, stock_price = simulate_stock_price(S0, mu, sigma,T=len(data))
        final_prices.append(stock_price[-1])

    expected_value = np.mean(final_prices)
    #generate a confidence interval
    confidence_interval = np.percentile(final_prices, [0.1,1,99, 99.9])
    return confidence_interval,expected_value
    print(f"Expected price: {expected_value}")
    print(f"1% confidence interval: [{confidence_interval[1]}, {confidence_interval[2]}]")
    print(f"0.1% confidence interval: [{confidence_interval[0]}, {confidence_interval[3]}]")

if __name__ == "__main__":
    import os
    files = os.listdir("data")
    for file in files:
        interval("data/"+file)