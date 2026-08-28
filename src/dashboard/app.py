import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from src.get_data import download_stock_data
from src.preprocess import preprocess
from src.anomaly_detection import detect_anomalies, get_top_anomalies

st.set_page_config(page_title="StockPulse", layout="wide")
st.title("📈 StockPulse - Stock Anomaly Detector")

st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker", value="AAPL")
start = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))
contamination = st.sidebar.slider("Contamination (anomaly %)", 0.01, 0.10, 0.05, 0.01)

run_button = st.sidebar.button("Run Analysis")

if run_button:
    with st.spinner("Fetching and processing data..."):
        raw_path = download_stock_data(ticker, str(start), str(end))
        df = preprocess(raw_path)
        df = df.reset_index()
        df = detect_anomalies(df, contamination=contamination)
        top_anomalies = get_top_anomalies(df)

    st.success(f"Analysis complete for {ticker}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Days", len(df))
    col2.metric("Anomalies Found", (df["Anomaly"] == -1).sum())
    col3.metric("Anomaly Rate", f"{(df['Anomaly'] == -1).mean()*100:.2f}%")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close Price"))

    fig.add_trace(go.Scatter(
        x=top_anomalies["Date"], y=top_anomalies["Close"],
        mode="markers", name="Anomaly",
        marker=dict(color="red", size=8, symbol="x")
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["MA_20"],
        mode="lines", name="MA 20",
        line=dict(dash="dot", color="orange")
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["MA_7"],
        mode="lines", name="MA 7",
        line=dict(dash="dot", color="green")
    ))
    fig.update_layout(title=f"{ticker} Price with Detected Anomalies", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Flagged Anomalies (sorted by magnitude)")
    st.dataframe(top_anomalies[["Date", "Close", "Return", "AbsReturn", "Volatility", "Volume"]])

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Full Results (CSV)", csv, f"{ticker}_anomalies.csv", "text/csv")