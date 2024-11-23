# charts.py
import yfinance as yf
import plotly.graph_objects as go
import json
import pandas as pd

def create_candlestick_chart(stock_symbol="AAPL"):
    # Fetch data for the past 1 year
    stock_data = yf.download(stock_symbol, period="5y", interval="1d")

    # print(stock_data)
    
    # Ensure we have data
    if stock_data.empty:
        return {"error": "No data found for this symbol"}
    
    
     # Flatten the index to convert it to a string (for JSON compatibility)
     
     # Reset index and ensure 'Date' is a column
    if 'Date' not in stock_data.columns:
        stock_data.reset_index(inplace=True)

    # Debugging: Check column names and first few rows
    # print(stock_data.columns)
    # print(stock_data.head())

        # Flatten multi-index columns if present
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in stock_data.columns]

    # print(stock_data.columns)  # Debugging step
    
    # Handle missing values
    stock_data.dropna(subset=['Open_AAPL', 'High_AAPL', 'Low_AAPL', 'Close_AAPL'], inplace=True)

    # Flattening all values
    # flattened_data = {
    #     key: [item[0] for item in stock_data['stock_data'][0][key]]
    #     for key in ['close', 'high', 'low', 'open']
    # }

    # print(flattened_data)

  # Extract individual columns
    dates = stock_data['Date_'].astype(str)
    open_prices = stock_data.get('Open_AAPL')
    high_prices = stock_data.get('High_AAPL')
    low_prices = stock_data.get('Low_AAPL')
    close_prices = stock_data.get('Close_AAPL')

    # Create a candlestick chart
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=dates,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=close_prices
            )
        ]
    )

    # Add title and layout configurations
    fig.update_layout(
        title=f"{stock_symbol} Candlestick Chart (5 Year)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    # Convert figure to JSON
    return json.loads(fig.to_json())
