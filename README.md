# Algo-trading-for-hedgefund
# 📈 BatraHedge Algo-Trading Hackathon – Stage 1 Submission
## Team Detail
**Team Name:** Fab 4  
**Members:**
- Amogh Nandwana - Keya Mehta - Rishit Modh  - Kavya Prajapati
  
---
- ## 🔍 Project Overview
- This project implements a **Moving Average Crossover algorithmic trading strategy** and performs **historical backtesting** using 5-minute equity market data provided by BatraHedge.
- The system is divided into:
1. **Algorithm & Backtesting Engine**
2. **Processed Backtest Outputs**
3. **Interactive Streamlit Web Dashboard**
- This separation reflects real-world algo trading platforms.
  
---
 ## 🧠 Strategy Description**Strategy:
 ** Moving Average Crossover  
 - **Fast MA:** 5-period
- **Slow MA:** 15-period

 ### Trading Logic-
 **Buy:** MA(5) crosses above MA(15)
 - **Sell:** MA(5) crosses below MA(15)
 
- **Hold:**
-  No crossoverSignals are applied on the next available 5-minute candle to simulate realistic execution.
---
  
## ⚙️ Backtesting Methodology
- Backtesting is performed using historical OHLC data.-
-  Trades are position-based (one trade at a time per stock).- No leverage, no transaction costs (educational simulation).
 - Key metrics calculated:
 - Cumulative Return
 - Total Trades
- Win Rate
- Maximum Drawdown
---
## 📊 Backtesting OutputsThe following files are generated after running the backtest:
| File Name | Description |
|----------|-------------|
| `raw_backtest_results.csv` | Candle-wise signals, returns, cumulative performance |
| `trade_log.csv` | Entry, exit, P&L of each trade |
| `config.json` | Strategy parameters used |
---
## 🖥️ Web Dashboard (UI)An interactive **Streamlit dashboard** is built on top of the backtest results.
### Features-
Multi-stock selection
-Date range filtering
- Price chart with moving averages
- Buy / Sell signal table
- Performance metrics
- CSV download option
---
## ▶️ How to Run the Project Locally
### Step 1: Prepare Data```bashpython prepare_clean_data.py
0 commit commentsComments0 (0)CommentSubscribeYou're not receiving notifications from this thread.
