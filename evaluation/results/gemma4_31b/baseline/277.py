import yfinance as yf
import pandas as pd
import folium
from datetime import datetime

def calculate_profitability():
    # 1. Список компаний: Тикер, Название, Координаты (Штаб-квартира)
    companies = {
        'AAPL': {'name': 'Apple', 'lat': 37.3346, 'lon': -122.0090},
        'MSFT': {'name': 'Microsoft', 'lat': 47.6397, 'lon': -122.1300},
        'GOOGL': {'name': 'Alphabet (Google)', 'lat': 37.4220, 'lon': -122.0841},
        'NVDA': {'name': 'NVIDIA', 'lat': 37.4050, 'lon': -121.9650},
        'TSM': {'name': 'TSMC', 'lat': 23.7870, 'lon': 120.9820},
        '005930.KS': {'name': 'Samsung Electronics', 'lat': 37.2636, 'lon': 127.1042},
        'ASML': {'name': 'ASML', 'lat': 52.0486, 'lon': 5.1228},
    }

    # Временной интервал: последние 30 лет
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now().year - 30)
    start_date_str = f"{start_date}-01-01"

    results = []

    print("Fetching financial data...")
    for ticker, info in companies.items():
        try:
            # Загрузка данных
            data = yf.download(ticker, start=start_date_str, end=end_date, progress=False)
            
            if not data.empty:
                # Берем первую и последнюю доступную цену закрытия
                price_start = data['Close'].iloc[0]
                price_end = data['Close'].iloc[-1]
                
                # Расчет доходности в процентах
                profitability = ((price_end - price_start) / price_start) * 100
                
                results.append({
                    'name': info['name'],
                    'ticker': ticker,
                    'profit': profitability,
                    'lat': info['lat'],
                    'lon': info['lon']
                })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    return results

def create_map(data):
    # Создаем карту, центрированную в середине мира
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

    for item in data:
        # Масштабирование радиуса круга для визуализации (логарифмический или линейный)
        # Чтобы избежать гигантских кругов для NVIDIA/Apple, используем корень или логарифм
        radius = max(5, (item['profit'] ** 0.5) * 0.5) if item['profit'] > 0 else 5
        
        # Цвет зависит от прибыльности
        color = 'green' if item['profit'] > 0 else 'red'

        folium.CircleMarker(
            location=[item['lat'], item['lon']],
            radius=radius,
            popup=f"<b>{item['name']}</b><br>Profitability: {item['profit']:.2f}%",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(m)

    # Сохранение карты
    m.save("277.html")
    print("Map has been saved as 277.html")

if __name__ == "__main__":
    # Выполнение моделирования
    profit_data = calculate_profitability()
    if profit_data:
        create_map(profit_data)
        
        # Вывод таблицы в консоль для проверки
        df = pd.DataFrame(profit_data)
        print("\nSummary of Profitability (Last 30 Years):")
        print(df[['name', 'profit']].sort_values(by='profit', ascending=False))
    else:
        print("No data retrieved.")