import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Upstox API configuration
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"

def get_historical_data(symbol, interval="1D", from_date=None, to_date=None):
    """Get historical stock data from Upstox API"""
    if not from_date:
        from_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")
        
    url = "https://api.upstox.com/v2/historical-candle"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "from_date": from_date,
        "to_date": to_date
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data['data'], 
                              columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calculate_bollinger_bands(df, window=20, num_std=2):
    """Calculate Bollinger Bands for the given dataframe"""
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper_Band'] = df['SMA'] + (df['STD'] * num_std)
    df['Lower_Band'] = df['SMA'] - (df['STD'] * num_std)
    return df

def analyze_stock(symbol):
    """Analyze stock using Bollinger Bands and provide buy/sell recommendation"""
    # Get historical data
    df = get_historical_data(symbol)
    if df is None:
        return
    
    # Calculate Bollinger Bands
    df = calculate_bollinger_bands(df)
    
    # Get latest values
    current_price = df['close'].iloc[-1]
    current_lower_band = df['Lower_Band'].iloc[-1]
    current_upper_band = df['Upper_Band'].iloc[-1]
    current_sma = df['SMA'].iloc[-1]
    
    # Calculate percentage distance from bands
    lower_band_distance = ((current_price - current_lower_band) / current_price) * 100
    upper_band_distance = ((current_upper_band - current_price) / current_price) * 100
    
    # Analysis
    print(f"\nAnalysis for {symbol}:")
    print(f"Current Price: {current_price:.2f}")
    print(f"20-day SMA: {current_sma:.2f}")
    print(f"Upper Band: {current_upper_band:.2f}")
    print(f"Lower Band: {current_lower_band:.2f}")
    
    # Decision making
    if current_price < current_lower_band:
        print("\nBUY SIGNAL:")
        print("Price is below lower Bollinger Band - potentially oversold")
        print(f"Price is {abs(lower_band_distance):.2f}% below the lower band")
        print("Consider buying but watch for confirmation of trend reversal")
        
    elif current_price > current_upper_band:
        print("\nSELL SIGNAL:")
        print("Price is above upper Bollinger Band - potentially overbought")
        print(f"Price is {upper_band_distance:.2f}% above the upper band")
        print("Consider selling or taking profits")
        
    else:
        print("\nNEUTRAL SIGNAL:")
        print("Price is within Bollinger Bands")
        print(f"Distance to upper band: {upper_band_distance:.2f}%")
        print(f"Distance to lower band: {abs(lower_band_distance):.2f}%")
        print("Monitor for breakout signals")

    # Additional trend analysis
    price_trend = "UPWARD" if current_price > current_sma else "DOWNWARD"
    print(f"\nPrice Trend: {price_trend}")
    print(f"Volatility: {df['STD'].iloc[-1]:.2f}")

# Example usage
if __name__ == "__main__":
    stock_symbol = "RELIANCE-EQ"  # Example stock symbol
    analyze_stock(stock_symbol)
