import requests
import pandas as pd
import folium

# Функция для получения данных о уровне воды из открытого источника (например, API)
def get_water_level_data():
    url = "https://api.example.com/water-levels?river=Ili"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch water level data")

# Функция для обработки данных
def process_data(data):
    df = pd.DataFrame(data)
    # Пример: преобразование времени в формат datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Функция для анализа данных и получения текущего уровня воды
def analyze_water_level(df):
    current_time = pd.Timestamp.now()
    current_data = df[df['timestamp'] == current_time]
    if not current_data.empty:
        return current_data['water_level'].values[0]
    else:
        raise Exception("No data available for the current time")

# Функция для визуализации данных на карте
def visualize_water_level(water_level, lat=42.1697, lon=73.5853):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Добавление маркера с уровнем воды
    folium.Marker(
        [lat, lon],
        popup=f"Текущий уровень воды: {water_level} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    m.save("1.html")
    return m

# Основной код
if __name__ == "__main__":
    try:
        data = get_water_level_data()
        df = process_data(data)
        water_level = analyze_water_level(df)
        print(f"Текущий уровень воды в реке Ili River: {water_level} м")
        
        # Визуализация данных
        m = visualize_water_level(water_level)
    except Exception as e:
        print(f"Ошибка: {e}")