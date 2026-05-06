import pandas as pd
import requests
from folium import Map, Marker

# Сбор данных
def get_stock_data(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/history"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data['prices'])

# Очистка данных
def clean_data(df):
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df

# Вычисление прибыльности
def calculate_profitability(df):
    df['profitability'] = (df['close'] - df['open'].shift()) / df['open'].shift() * 100
    df['profitability'] = df['profitability'].fillna(0)
    return df

# Агрегация данных
def aggregate_data(df):
    df = df.resample('Y').mean()
    return df

# Визуализация данных
def visualize_data(df, companies):
    m = Map(location=[37.7749, -122.4194], zoom_start=5)
    for company in companies:
        stock_data = get_stock_data(company)
        cleaned_data = clean_data(stock_data)
        profitable_data = calculate_profitability(cleaned_data)
        aggregated_data = aggregate_data(profitable_data)
        avg_profitability = aggregated_data['profitability'].mean()
        Marker([37.7749, -122.4194], popup=f"{company}: {avg_profitability:.2f}%").add_to(m)
    m.save("277.html")

# Список компаний в технологическом секторе
companies = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

visualize_data(companies)