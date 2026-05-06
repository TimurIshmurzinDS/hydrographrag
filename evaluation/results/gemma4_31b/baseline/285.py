import pandas as pd
import numpy as np
import yfinance as yf
import folium
from folium.plugins import MarkerCluster

def calculate_rsi(data, window=14):
    diff = data.diff(1)
    gain = (diff.where(diff > 0, 0)).rolling(window=window).mean()
    loss = (-diff.where(diff < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def backtest_sma(data):
    # SMA Crossover Strategy
    sma_short = data['Close'].rolling(window=20).mean()
    sma_long = data['Close'].rolling(window=50).mean()
    
    # Signal: 1 for long, 0 for neutral
    signal = np.where(sma_short > sma_long, 1, 0)
    returns = data['Close'].pct_change() * pd.Series(signal).shift(1).values
    return (1 + returns).prod() - 1

def backtest_rsi(data):
    # RSI Mean Reversion Strategy
    rsi = calculate_rsi(data['Close'])
    
    # Signal: Buy when RSI < 30, Sell when RSI > 70
    signal = np.zeros(len(data))
    position = 0
    for i in range(len(rsi)):
        if rsi.iloc[i] < 30:
            position = 1
        elif rsi.iloc[i] > 70:
            position = 0
        signal[i] = position
        
    returns = data['Close'].pct_change() * pd.Series(signal).shift(1).values
    return (1 + returns).prod() - 1

# 1. Define assets and their coordinates
assets_geo = {
    '^GSPC': {'name': 'S&P 500 (USA)', 'coords': [37.0902, -95.7129]},
    '^GDAXI': {'name': 'DAX (Germany)', 'coords': [51.1657, 10.4515]},
    '^N225': {'name': 'Nikkei 225 (Japan)', 'coords': [36.2048, 138.2529]},
    '^FTSE': {'name': 'FTSE 100 (UK)', 'coords': [55.3781, -3.4360]},
    '^HSI': {'name': 'Hang Seng (HK)', 'coords': [22.3193, 114.1694]},
}

results = []

# 2. Process data and run strategies
for ticker, info in assets_geo.items():
    df = yf.download(ticker, period='1y', progress=False)
    if df.empty: continue
    
    sma_perf = backtest_sma(df)
    rsi_perf = backtest_rsi(df)
    
    results.append({
        'ticker': ticker,
        'name': info['name'],
        'coords': info['coords'],
        'sma_perf': sma_perf,
        'rsi_perf': rsi_perf
    })

# 3. GIS Visualization
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

for res in results:
    # Determine color based on the average performance of both strategies
    avg_perf = (res['sma_perf'] + res['rsi_perf']) / 2
    color = 'green' if avg_perf > 0 else 'red'
    
    popup_text = (
        f"<b>{res['name']}</b><br>"
        f"SMA Strategy: {res['sma_perf']:.2%}<br>"
        f"RSI Strategy: {res['rsi_perf']:.2%}"
    )
    
    folium.CircleMarker(
        location=res['coords'],
        radius=10,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Save the map
m.save("285.html")

print("Analysis complete. The results are visualized in 285.html")