# Crypto Bot / BackTesting Project

## Problem Statement:

The Stock and Crypto market is very scary and unpredictable. What do I buy? How much do I buy? Why do I keep losing money? Are all very common question when entering the market. Unfortunately, the answer to all these questions is "It depends." I was brought on by JPMorgan to analyze specifically the Crypto Market and discover possible investment strategies that would make the Crypto Market worth it. The goal of this specific project is to give you an edge by giving you a platform to create candle stick trend analysis strategies and a machine learning forecaster that predicts the close price of a specific crypto currency. This will help you understand when to enter the market and when to leave the market. The main objective is to maximize your gains in your "wallet" or alternatively minimize your losses in your "wallet" while simultaneously maximizing the shares you have. The reason I say the second part in my objective is because Investment isn’t fast cash, it takes time. The market is so volatile so even when you have invested in a cryptocurrency that is tanking you are concurrently increasing the number of shares you have within that cryptocurrency. So, if the market were to ever go back up your wallet is now in a better position.

## Process:

The process I took to create this project started with research. While initially using the platform Trade View I started testing around with several prebuilt functions and strategies created by the community. After testing different strategies I realized that adapting a backtester for these strategies and bot for automated trades was a good idea to have customizable environment to understand these strategies performance.

This led me to create a Bot that pulls live crypto candle stick data from the API Binance and run 3 different strategies.

1. PSAR, MACD, EMA
2. RSI, EMA, SUPERTREND
3. HOFFMAN

After successfully getting a buy and sell signals for all of these strategies I decided to design a Database so I could save this information to run later. I had to create a ETL Pipeline that would go from:

- Binance -> Historical candle stick table -> Strategy Table -> Buy and Sell Signals Table

Tickers Used:

- ADA - https://coinmarketcap.com/currencies/cardano/
- ONE - https://coinmarketcap.com/currencies/harmony/
- HBAR - https://coinmarketcap.com/currencies/hedera/
- VET - https://coinmarketcap.com/currencies/vechain/
- LTC - https://coinmarketcap.com/currencies/litecoin/
- BCH - https://coinmarketcap.com/currencies/bitcoin-cash/
- ETH - https://coinmarketcap.com/currencies/ethereum/

**Note**: I hosted my database locally until I built my back testing application.

After obtaining a good sum of data I decided I wanted to see the performance of these strategies and began creating my back tester Streamlit web application. I adapted the same functions and Database connections I used for my bot and additional added wallet functionality, graphics, timeseries prediction neural network, and downloading data functionality. Once my back tester application was complete, I was able to analyze the performance of these strategies over time and see how they would affect my wallet balance if I started with 500 USD.

## Conclusion:

In conclusion the three strategies I used were effective. Their following preformance made me understand certain strategies strengths and weaknesses. It is a difficult time to test a trading bot when almost every market is down 10 - 40 percent. However, my findings were that the PSAR + MACD + EMA and HOFFMAN strategies greatly out preformed RSI + EMA + SUPERTREND. With a starting wallet of 500 USD, I on average lost 20 percent and gained on average 5 percent. After further review I noticed that PSAR + MACD + EMA and HOFFMAN strategies really excel when the market is consistently trending if the market is inconsistent, they may make bad trades. Alternatively, for the RSI + EMA + SUPERTREND the performance was terribly with little to no buy or sell signals which may mean it needs some refactoring before testing again. Additionally, in terms of my timeseries Neural Networks (NN) that I implemented the...

PSAR + MACD + EMA NN preformance:

- loss: 0.0036
- mean_absolute_error: 0.0463
- val_loss: 0.0121
- val_mean_absolute_error: 0.0841

RSI + EMA + SUPERTREND preformance:

- loss: 0.0235
- mean_absolute_error: 0.1215
- val_loss: 0.0176
- val_mean_absolute_error: 0.1063

HOFFMAN preformance:

- loss: 0.1175
- mean_absolute_error: 0.2671
- val_loss: 0.1309
- val_mean_absolute_error: 0.2869

There scores were low but when testing with live trades performance seemed questionable. However, they did seem to follow the general trend which is a good sign. Regardless, I believe my strategies and my NN's greatly reduced the amount of loss an trader would see in investing aimlessly. Not only did I choose unknown cryptocurrencies, but I was still able to reduce my losses and maximize some gains. With a little finer tuning and adding more complex strategies I believe it’s possible to discover investment strategies that would make the Crypto Market worth it.

## Future Improvements:

- Improve ETL Pipeline.
- Adapt Bot to Raspberry Pi.
- Add additional Strategies.
- Reformat Database.
- Improve models performance with more feature engineering.
- Migrate strategies to stock.
- Implement user input model prediction page

## Outside Resources:

- https://www.tradingview.com/chart/Bly58aYC/
- Japanese CandleStick Charting Techniques - Second Edition, written by Steve Nison
- https://www.best-trading-platforms.com/trading-platform-futures-forex-cfd-stocks-nanotrader/rob-hoffmans-inventory-retracement-trades
- https://www.investopedia.com/terms/r/rsi.asp
- https://www.investopedia.com/terms/e/ema.asp
- https://www.elearnmarkets.com/blog/supertrend-indicator-strategy-trading/#:~:text=web.stockedge.com-,Key%20Takeaways,accurate%20signals%20on%20precise%20time
- https://www.investopedia.com/terms/p/parabolicindicator.asp
- https://www.investopedia.com/terms/m/macd.asp
- https://www.investopedia.com/terms/e/ema.asp

## How to run:

1. Create conda env and activate and install pip.

```
conda create --name <envname>
conda activate <envname>
conda install pip
```

2. Navigate to project repo Install requirments.txt.

```
pip install -r requirements.txt
```

3. Run application

- Note: Navigate to the correct directory and

For those getting odd path references in requirements.txt, use:

```
pip list --format=freeze > requirements.txt
```

1. Navigate to ./Compenent/Bot

- Note run on a 15 min interval to get most accurate preformance

```
python run_bot.py
```

#### or

4. Navigate to ./Compenent/Backtester

```
streamlit run backtester.py
```

5. Enjoy :)
