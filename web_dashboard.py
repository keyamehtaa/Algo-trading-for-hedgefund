import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="BatraHedge Algo Trading Dashboard",
    layout="wide"
)
st.set_page_config(page_title="BatraHedge Algo Dashboard", layout="wide")

st.title("📈 BatraHedge Algo-Trading Dashboard")
st.markdown("Moving Average Crossover Strategy (MA 5 / MA 15)")

# -------------------------
# Load Data
# -------------------------
# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    df = pd.read_csv("raw_backtest_results.csv")
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    return df
    return pd.read_csv("raw_backtest_results.csv", parse_dates=["Datetime"])

df = load_data()

# -------------------------
# Sidebar Controls
# -------------------------
# ===================== SIDEBAR =====================
st.sidebar.header("🔧 Controls")

symbols = sorted(df["tradingsymbol"].unique())
selected_symbol = st.sidebar.selectbox("Select Stock", symbols)
stocks = sorted(df["tradingsymbol"].unique())
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

symbol_df = df[df["tradingsymbol"] == selected_symbol].copy()
stock_df = df[df["tradingsymbol"] == selected_stock].copy()

start_date = st.sidebar.date_input(
    "Start Date", symbol_df["Datetime"].min().date()
)
end_date = st.sidebar.date_input(
    "End Date", symbol_df["Datetime"].max().date()
min_date = stock_df["Datetime"].min()
max_date = stock_df["Datetime"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

symbol_df = symbol_df[
    (symbol_df["Datetime"].dt.date >= start_date) &
    (symbol_df["Datetime"].dt.date <= end_date)
stock_df = stock_df[
    (stock_df["Datetime"] >= pd.to_datetime(date_range[0])) &
    (stock_df["Datetime"] <= pd.to_datetime(date_range[1]))
]

# -------------------------
# Metrics
# -------------------------
final_return = symbol_df["cumulative_return"].iloc[-1]
total_trades = symbol_df["signal"].abs().sum()
max_dd = symbol_df["drawdown"].min()

col1, col2, col3 = st.columns(3)
col1.metric("📊 Final Cumulative Return", f"{final_return:.4f}")
col2.metric("🔁 Total Trades", int(total_trades))
col3.metric("⚠️ Max Drawdown", f"{max_dd:.4f}")

# -------------------------
# Price Chart
# -------------------------
st.subheader("📉 Price Chart with Moving Averages")
# ===================== METRICS =====================
total_trades = stock_df["signal"].abs().sum()
final_return = stock_df["cumulative_return"].iloc[-1]

chart_df = symbol_df.set_index("Datetime")[["close", "ma_fast", "ma_slow"]]
st.line_chart(chart_df)
drawdown = (stock_df["cumulative_return"] /
            stock_df["cumulative_return"].cummax()) - 1
max_drawdown = drawdown.min()

# -------------------------
# Buy / Sell Signals
# -------------------------
st.subheader("🟢 Buy / 🔴 Sell Signals")

signal_df = symbol_df[symbol_df["signal"] != 0][
    ["Datetime", "close", "signal"]
]

st.dataframe(signal_df, use_container_width=True)
col1, col2, col3 = st.columns(3)
col1.metric("Final Cumulative Return", f"{final_return:.4f}")
col2.metric("Total Trades", int(total_trades))
col3.metric("Max Drawdown", f"{max_drawdown:.2%}")

# ===================== PRICE CHART =====================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=stock_df["Datetime"],
    y=stock_df["close"],
    mode="lines",
    name="Close Price"
))

fig.add_trace(go.Scatter(
    x=stock_df["Datetime"],
    y=stock_df["ma_fast"],
    mode="lines",
    name="MA 5"
))

fig.add_trace(go.Scatter(
    x=stock_df["Datetime"],
    y=stock_df["ma_slow"],
    mode="lines",
    name="MA 15"
))

# Buy signals
buy_df = stock_df[stock_df["signal"] == 1]
sell_df = stock_df[stock_df["signal"] == -1]

fig.add_trace(go.Scatter(
    x=buy_df["Datetime"],
    y=buy_df["close"],
    mode="markers",
    marker=dict(color="green", size=8),
    name="BUY"
))

fig.add_trace(go.Scatter(
    x=sell_df["Datetime"],
    y=sell_df["close"],
    mode="markers",
    marker=dict(color="red", size=8),
    name="SELL"
))

fig.update_layout(
    title=f"{selected_stock} Price Chart with Signals",
    xaxis_title="Time",
    yaxis_title="Price",
    height=600
)

# -------------------------
# Raw Data
# -------------------------
with st.expander("📄 View Raw Backtest Data"):
    st.dataframe(symbol_df.tail(200), use_container_width=True)
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Download
# -------------------------
# ===================== DOWNLOAD =====================
st.download_button(
    "⬇️ Download Backtest CSV",
    symbol_df.to_csv(index=False),
    file_name=f"{selected_symbol}_backtest.csv"
    label="⬇ Download Backtest CSV",
    data=stock_df.to_csv(index=False),
    file_name=f"{selected_stock}_backtest.csv",
    mime="text/csv"
)

st.success("✅ Dashboard loaded successfully")
