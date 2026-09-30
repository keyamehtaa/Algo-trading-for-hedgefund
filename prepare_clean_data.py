import pandas as pd

# Load your full dataset
df = pd.read_excel("power_equity_zerodha_5minute .xlsx")

# Combine date and time if separate
df['Datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

# Keep only necessary columns
df = df[['Datetime', 'tradingsymbol', 'close']].copy()

results = []

# Loop through each stock
for symbol in df['tradingsymbol'].unique():
    temp = df[df['tradingsymbol'] == symbol].copy()
    temp = temp.sort_values('Datetime')

    # Moving averages
    temp['MA_5'] = temp['close'].rolling(5).mean()
    temp['MA_15'] = temp['close'].rolling(15).mean()

    # Signals
    temp['signal'] = 0
    temp.loc[temp['MA_5'] > temp['MA_15'], 'signal'] = 1
    temp.loc[temp['MA_5'] < temp['MA_15'], 'signal'] = -1

    # Backtest
    temp['return'] = temp['close'].pct_change()
    temp['strategy_return'] = temp['return'] * temp['signal'].shift(1)
    temp['cumulative_return'] = (1 + temp['strategy_return']).cumprod()

    results.append(temp)

# Combine all stocks
final_df = pd.concat(results)
final_df.to_csv("final_clean_backtest.csv", index=False)
print("✅ All stocks processed and saved to final_clean_backtest.csv")
