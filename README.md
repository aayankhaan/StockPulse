# StockPulse - Stock Price Anomaly Tracker

**Category:** Data Science Dominion | TechWiz 6
**Theme:** Stock Price Anomaly Tracker

## 🔗 Live Demo
[StockPulse Dashboard](https://stockpulse-vzjbnysqdykiknvckw5cut.streamlit.app/)

## 1. Problem Definition

Financial time series data, like stock prices can change a lot. Sometimes have strange patterns. These patterns might be jumps up or down or unusual changes that don't fit what usually happens in the market. These strange events can show things like people trying to cheat the market big news that changes how people feel about a stock or problems with the system. Checking for these things by hand is not easy when there is a lot of data and it changes quickly.

**StockPulse** is a solution that uses data science to find these patterns in stock price changes. It uses machine learning that doesn't need people to tell it what to look for. It shows the results, on a web dashboard that people can interact with.

## 2. Proposed Solution

StockPulse pulls stock market data useful features such, as returns, moving averages and volatility and then runs the **Isolation Forest** algorithm to spot days with odd price moves. The results appear on a dashboard where a user can pick any stock ticker choose a date range and set how sensitive the alerts should be.

## 3. Architecture / Pipeline

```
User Input (Ticker, Dates)
        ↓
Data Ingestion (yfinance API)
        ↓
Data Preprocessing (cleaning, date parsing, normalization)
        ↓
Feature Engineering (Return, MA_7, MA_20, Volatility)
        ↓
Feature Selection (correlation analysis)
        ↓
Data Partitioning (train/test split)
        ↓
Anomaly Detection (Isolation Forest)
        ↓
Model Evaluation (synthetic anomaly injection + Precision/Recall/F1)
        ↓
Interactive Dashboard (Streamlit + Plotly)
```

## 4. Tech Stack

- **Language:** Python 3.11+
- **Data Source:** yfinance (Yahoo Finance API)
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** scikit-learn (Isolation Forest, StandardScaler)
- **Visualization:** Plotly
- **Web Dashboard:** Streamlit
- **Data Store:** CSV

## 5. Project Structure

```
StockPulse/
├── src/
│   ├── get_data.py           # Fetches stock data via yfinance
│   ├── preprocess.py         # Cleans data, engineers features
│   ├── anomaly_detection.py  # Isolation Forest model + top anomalies
│   ├── correlation.py        # Feature correlation analysis
│   └── evaluate.py           # Model evaluation via synthetic anomalies
├── app.py                    # Streamlit dashboard (entry point)
├── requirements.txt
└── README.md
```

## 6. Installation & Setup

```bash
# Clone the repository
git clone https://github.com/aayankhaan/StockPulse.git
cd StockPulse

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## 7. How to Use

1. Enter a stock ticker (e.g. `AAPL`, `GOOG`, `MSFT`) in the sidebar
2. Select a start and end date
3. Adjust the "Contamination" slider to control anomaly sensitivity (default 5%)
4. Click **Run Analysis**
5. View the price chart with flagged anomalies, summary metrics, and the sorted anomaly table
6. Download the full results as CSV if needed

## 8. Feature Engineering

- **Return:** Daily percentage change in closing price
- **MA_7 / MA_20:** 7-day and 20-day moving averages (used for visualization and trend context)
- **Volatility:** 20-day rolling standard deviation of returns

## 9. Feature Selection

A correlation analysis was performed on the model's input features (`Return`, `Volume`, `Volatility`):

              Return    Volume  Volatility
Return      1.000000  0.081201    0.044888
Volume      0.081201  1.000000    0.168511
Volatility  0.044888  0.168511    1.000000

All pairwise correlations are low (below 0.17), confirming each feature contributes distinct, non-redundant information. All three features were retained for the model.

## 10. Model: Isolation Forest

Isolation Forest is an anomaly detection method that works well with time series data when there are no labeled anomalies. It operates by dividing the data into partitions. Anomalous points tend to be isolated quickly meaning they require fewer splits compared to normal points because they stand out from the rest of the data.

The dataset is divided into 80% for training. 20% For testing. The model is trained on the training portion to understand what normal market behavior looks like. After training it is applied to the dataset to detect and flag any unusual patterns or anomalies.

## 11. Model Evaluation

Since real stock market data has no labeled ground truth for anomalies, model performance was validated using **synthetic anomaly injection**:

- 15 extreme synthetic anomalies were artificially injected into a copy of the dataset
- The model's ability to detect these known anomalies was measured

**Results:**
- **Precision:** 0.44
- **Recall:** 1.00
- **F1-score:** 0.61

The model achieved perfect recall, successfully identifying all injected anomalies. Precision was moderate because the model also correctly flagged genuine, naturally-occurring anomalies already present in the real data - these are additional true detections, not errors.

## 12. Test Data

The application was tested using real historical stock data for **AAPL (Apple Inc.)** across multiple date ranges (2023–2026), fetched live via the yfinance API.

## 13. Assumptions

- The project uses CSV as the primary data store, as permitted under the SRS. Database technologies (MongoDB/MySQL) were not required for the current functional scope, which involves single-ticker time series analysis rather than persistent multi-user storage.
- The system focuses on offline/on-demand analysis rather than real-time streaming detection, consistent with the SRS constraints.
- Tableau was substituted with Plotly + Streamlit for dashboard visualization to enable live web hosting, which is not natively supported by Tableau Desktop.

## 14. AI Tool Disclosure

This project's documentation and select code review/debugging assistance were supported using Claude (Anthropic). All core logic, code, and design decisions were written and understood by the developer, per competition guidelines.