# Crypto Bot / BackTesting Project

## Problem Statement:

The Stock and Crypto market is very scary and unpredictable. What do I buy? How much do I buy? Why do I keep losing money? Are all very common question when entering the market. Unfortunately, the answer to all these questions is "It depends." The goal of this specific project is to give you an edge by giving you a platform to create candle stick trend analysis strategies and a machine learning forecaster that predicts the close price to help you understand when to enter the market and when to leave the market. The main objective is to maximize your gains in your "wallet" or alternatively minimize your losses in your "wallet".

## Process:

The process I took to create this project started with research. While initially using the platform Trade View I started testing around with several prebuilt functions and strategies created by the community. After testing different strategies I realized that adapting a back testing for these strategies and bot for automated trades was a good idea to have customized environment to understand these strategies performance.

This led me to create a Bot that pulls live crypto candle stick data from the API Binance and run 3 different strategies.

1. PSAR, MACD, EMA
2. RSI, EMA, SUPERTREND
3. HOFFMAN

After successfully getting a buy and sell signals for all of these strategies I decided to design a Database so I could save this information to run later. I had to create a ETL Pipeline that would go from:

- Binance -> Historical candle stick table -> strategy table -> buy and sell signals table

Tickers Used:

- ADA - https://coinmarketcap.com/currencies/cardano/
- ONE - https://coinmarketcap.com/currencies/harmony/
- HBAR - https://coinmarketcap.com/currencies/hedera/
- VET - https://coinmarketcap.com/currencies/vechain/
- LTC - https://coinmarketcap.com/currencies/litecoin/
- BCH - https://coinmarketcap.com/currencies/bitcoin-cash/
- ETH - https://coinmarketcap.com/currencies/ethereum/

**Note**: I hosted my database locally until I built my back testing application.

After obtaining a good sum of data I decided I wanted to see the performance of these strategies and began creating my back tester Streamlit web application. I adapted the same functions and Database connections I used for my bot and additional added SQLAlchemy, wallet functionality, graphics, timeseries prediction neural network, and downloading data functionality. Once my back tester application was complete, I was able to analyze the performance of these strategies over time and see how they would affect my wallet balance if I started with 500 USD.

## Conclusion:

In conclusion the three strategies I used were effective. My application made me understand certain strategies strengths and weaknesses. It is a difficult time to test a trading bot when almost every market is down 10 - 40 percent. However, my findings were that the PSAR + MACD + EMA and HOFFMAN strategies greatly out preformed RSI + EMA + SUPERTREND. With a starting wallet of 500 USD, I on average lost 20 percent and gained on average 5 percent. After further review I noticed that PSAR + MACD + EMA and HOFFMAN strategies really excel when the market is consistently trending if the market is inconsistent, they may make bad trades. Alternatively, for the RSI + EMA + SUPERTREND the performance was terribly with little to no buy or sell signals which may mean it needs some refactoring before testing again. Additionally, in terms of my timeseries Neural Networks (NN) that I implemented the PSAR + MACD + EMA NN preformed with a mean absolute error of 0.0970, the RSI + EMA + SUPERTREND performed with a mean absolute error of 0.0224, and the HOFFMAN NN preformed with a mean absolute error of 0.0343. There scores were low but when testing with live trades performance seemed questionable. Regardless, I believe my strategies and my NN's greatly reduced the amount of loss an average trader would see in investing aimlessly. Not only did I choose unknown crypto currencies, but I was still able to reduce my losses and maximize some gains.

## Future Improvements:

- Improve ETL Pipeline.
- Adapt Bot to Raspberry Pi.
- Add additional Strategies.
- Reformat Database.
- Improve models performance with more feature engineering.
- Migrate strategies to stock.

## Outside Resources:

- https://www.tradingview.com/chart/Bly58aYC/

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

#### Bot

```
python3 bot.py
```

#### BackTester Application

```
streamlit run backtester.py
```

For those getting odd path references in requirements.txt, use:

```
pip list --format=freeze > requirements.txt
```
