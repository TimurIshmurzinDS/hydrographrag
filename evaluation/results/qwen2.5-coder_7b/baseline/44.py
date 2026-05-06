import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'latitude': [43.123, 43.124, 43.125, 43.126],
    'longitude': [70.123, 70.124, 70.125, 70.126],
    'pH': [7.2, 7.3, 7.4, 7.5],
    'temperature': [18, 19, 20, 21]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[43.124, 70.124], zoom_start=15)

# Добавление теплового слоя для показателя pH
HeatMap(df[['latitude', 'longitude', 'pH']], radius=15).add_to(m)

# Добавление маркеров для других показателей
for idx, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"pH: {row['pH']}, Температура: {row['temperature']}").add_to(m)

# Сохранение карты
m.save("44.html")