# Stock Price Prediction Telegram Bot

This project is a Telegram bot that predicts stock prices using Geometric Brownian Motion (GBM) and sends the confidence intervals to a specified chat.

## Features

The bot supports the following commands:

- `/ping`: The bot responds with "pong".
- `/interval`: The bot downloads the specified stock's data, calculates the expected price and confidence intervals, and sends them to the chat.

## Usage

To use the bot, you need to set up your telegram bot key and chat ID in `BOT_KEY.txt` and `telegram_chat_id.txt`, respectively.

Then, you can start the bot and send commands in the following format:

- `/interval <ticker> -tf <timeframe> -p <period>`
- `/trade <ticker>`

Where:
- `<ticker>` is the stock ticker symbol.
- `<timeframe>` is the timeframe for the data (default is "D" for daily).
- `<period>` is the lookback period for the data (default is 1).

## Dependencies

This project depends on the following Python libraries:

- `telebot`
- `oandapyV20` (could be replaced with `yfinance`` for stock data)

## Disclaimer

This bot is for educational purposes only. It should not be used for making real-world investment decisions.