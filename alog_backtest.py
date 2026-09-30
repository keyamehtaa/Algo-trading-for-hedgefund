import pandas as pd
import numpy as np
import json
import os

# ---------------------------------------------------
# LOAD CLEAN DATA
# ---------------------------------------------------
INPUT_FILE = "final_clean_backtest.csv"  # your cleaned dataset
OUTPUT_RESULTS = "raw_backtest_results.csv"
OUTPUT_TRADES = "trade_log.csv"
OUTPUT_CONFIG = "config.json"

df = pd.read_csv(INPUT_FILE, parse_dates=["Datetime"])

# ---------------------------------------------------
# STRATEGY PARAMETERS
# ---------------------------------------------------
FAST_MA = 5
SLOW_MA = 15

config = {
    "strategy": "Moving Average Crossover",
    "fast_ma": FAST_MA,
    "slow_ma": SLOW_MA,
    "timeframe": "5-minute",
    "execution": "next candle"
}

# ---------------------------------------------------
# CONTAINERS
# ---------------------------------------------------
all_results = []
all_trades = []

# ---------------------------------------------------
# RUN BACKTEST PER STOCK
# ---------------------------------------------------
for symbol in df["tradingsymbol"].unique():

    data = df[df["tradingsymbol"] == symbol].copy()
    data = data.sort_values("Datetime")

    data["ma_fast"] = data["close"].rolling(FAST_MA).mean()
    data["ma_slow"] = data["close"].rolling(SLOW_MA).mean()

    data["signal"] = 0
    data.loc[data["ma_fast"] > data["ma_slow"], "signal"] = 1
    data.loc[data["ma_fast"] < data["ma_slow"], "signal"] = -1

    data["position"] = data["signal"].shift(1).fillna(0)

    data["returns"] = data["close"].pct_change().fillna(0)
    data["strategy_returns"] = data["returns"] * data["position"]

    data["cumulative_return"] = (1 + data["strategy_returns"]).cumprod()
    data["drawdown"] = data["cumulative_return"] / data["cumulative_return"].cummax() - 1

    # ---------------- TRADE LOG ----------------
    entry_price = None
    entry_time = None

    for i in range(1, len(data)):
        if data.iloc[i]["position"] == 1 and data.iloc[i - 1]["position"] == 0:
            entry_price = data.iloc[i]["close"]
            entry_time = data.iloc[i]["Datetime"]

        elif data.iloc[i]["position"] == 0 and data.iloc[i - 1]["position"] == 1:
            exit_price = data.iloc[i]["close"]
            exit_time = data.iloc[i]["Datetime"]

            pnl = (exit_price - entry_price) / entry_price

            all_trades.append({
                "tradingsymbol": symbol,
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl
            })

    all_results.append(data)

# ---------------------------------------------------
# SAVE FILES
# ---------------------------------------------------
final_results = pd.concat(all_results)
final_results.to_csv(OUTPUT_RESULTS, index=False)

trade_df = pd.DataFrame(all_trades)
trade_df.to_csv(OUTPUT_TRADES, index=False)

with open(OUTPUT_CONFIG, "w") as f:
    json.dump(config, f, indent=4)

print("✅ Backtest completed successfully")
print("Files generated:")
print("✔ raw_backtest_results.csv")
print("✔ trade_log.csv")
print("✔ config.json")
