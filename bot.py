import yfinance as yf
import pandas as pd
import json
import os
import time
from datetime import datetime

START_BALANCE = 100.0

SYMBOLS = [
    "AAPL",
    "TSLA",
    "AMD",
    "SPY"
]

POSITION_SIZE = 0.25

def load_stats():
    if os.path.exists("stats.json"):
        with open("stats.json", "r") as f:
            return json.load(f)

    return {
        "balance": START_BALANCE,
        "wins": 0,
        "losses": 0,
        "trades": 0
    }

def save_stats(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)

def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            return json.load(f)
    return [START_BALANCE]

def save_history(history):
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)

def load_trades():
    if os.path.exists("trades.json"):
        with open("trades.json", "r") as f:
            return json.load(f)
    return []

def save_trades(trades):
    with open("trades.json", "w") as f:
        json.dump(trades, f, indent=4)

def get_signal(symbol):
    try:
        df = yf.download(
            symbol,
            period="5d",
            interval="15m",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 30:
            return None

        df["EMA9"] = df["Close"].ewm(span=9).mean()
        df["EMA21"] = df["Close"].ewm(span=21).mean()

        last = df.iloc[-1]

        if last["EMA9"] > last["EMA21"]:
            return "BUY"

        return "SELL"

    except Exception as e:
        print(e)
        return None

stats = load_stats()
history = load_history()
trades = load_trades()

print("APEX Lite Started")

while True:

    for symbol in SYMBOLS:

        signal = get_signal(symbol)

        if signal == "BUY":

            trade_size = stats["balance"] * POSITION_SIZE

            pnl_percent = 0.01

            profit = trade_size * pnl_percent

            stats["balance"] += profit
            stats["wins"] += 1
            stats["trades"] += 1

            history.append(round(stats["balance"], 2))

            trades.append({
                "time": str(datetime.now()),
                "symbol": symbol,
                "result": "WIN",
                "profit": round(profit, 2)
            })

            print(f"{symbol} WIN +${profit:.2f}")

        elif signal == "SELL":

            trade_size = stats["balance"] * POSITION_SIZE

            pnl_percent = -0.005

            loss = trade_size * abs(pnl_percent)

            stats["balance"] -= loss
            stats["losses"] += 1
            stats["trades"] += 1

            history.append(round(stats["balance"], 2))

            trades.append({
                "time": str(datetime.now()),
                "symbol": symbol,
                "result": "LOSS",
                "profit": round(-loss, 2)
            })

            print(f"{symbol} LOSS -${loss:.2f}")

        save_stats(stats)
        save_history(history)
        save_trades(trades)

    time.sleep(300)
