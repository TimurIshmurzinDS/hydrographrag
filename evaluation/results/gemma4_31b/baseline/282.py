import pandas as pd
import numpy as np
import yfinance as yf
import folium
from folium.plugins import HeatMap

def predict_crypto_drop():
    # 1. Fetch Cryptocurrency Data (Bitcoin)
    print("Fetching market data...")
    ticker = "BTC-USD"
    data = yf.download(ticker, period="60d", interval="1d")
    
    if data.empty:
        print("Error fetching data")
        return

    # 2. Volatility Analysis
    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change()
    
    # Calculate rolling volatility (7-day window)
    window = 7
    data['Volatility'] = data['Returns'].rolling(window=window).std()
    
    # Calculate the threshold for "High Risk" (Mean + 1 Std Dev of volatility)
    avg_vol = data['Volatility'].mean()
    std_vol = data['Volatility'].std()
    threshold = avg_vol + std_vol
    
    current_vol = data['Volatility'].iloc[-1]
    
    # Prediction Logic
    if current_vol > threshold:
        risk_level = "HIGH"
        color = "red"
        status = "Potential Price Drop Predicted (High Volatility)"
    elif current_vol > avg_vol:
        risk_level = "MEDIUM"
        color = "orange"
        status = "Increased Volatility (Caution)"
    else:
        risk_level = "LOW"
        color = "green"
        status = "Stable Market"

    print(f"Current Volatility: {current_vol:.4f} | Threshold: {threshold:.4f}")
    print(f"Prediction: {status}")

    # 3. Geospatial Integration
    # Coordinates of major Crypto-Financial Hubs
    hubs = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "weight": 10},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "weight": 8},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "weight": 9},
        {"name": "Tokyo", "lat": 35.6895, "lon": 139.6917, "weight": 7},
        {"name": "Seoul", "lat": 37.5665, "lon": 126.9780, "weight": 8},
        {"name": "Frankfurt", "lat": 50.1109, "lon": 8.6821, "weight": 6},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "weight": 8},
        {"name": "Zug (Crypto Valley)", "lat": 47.275, "lon": 8.517, "weight": 5},
    ]

    # 4. Map Visualization
    # Initialize map centered on the world
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

    # Add markers for hubs based on the global volatility risk
    for hub in hubs:
        folium.CircleMarker(
            location=[hub["lat"], hub["lon"]],
            radius=hub["weight"] * 2,
            popup=f"{hub['name']} - Risk: {risk_level}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

    # Add a global status legend as a text element (via HTML)
    title_html = f'''
       <div style="position: fixed; 
                   bottom: 50px; left: 50px; width: 300px; height: 90px; 
                   z-index: 9999; font-size: 14px; 
                   background-color: white; padding: 10px; 
                   border: 2px solid black; border-radius: 10px;">
       <b>Crypto Volatility Monitor</b><br>
       Current Status: <span style="color:{color}; font-weight:bold;">{status}</span><br>
       Volatility Index: {current_vol:.4f}
       </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Save the map
    m.save("282.html")
    print("Map has been saved as 282.html")

if __name__ == "__main__":
    predict_crypto_drop()