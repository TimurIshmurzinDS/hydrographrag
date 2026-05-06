import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных о темпах инфляции для различных регионов вдоль реки Sharyn River
data = {
    'latitude': [54.123, 54.234, 54.345, 54.456, 54.567],
    'longitude': [60.123, 60.234, 60.345, 60.456, 60.567],
    'inflation_rate': [3.2, 3.5, 3.8, 4.1, 4.4]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Создаем карту с центром вдоль реки Sharyn River
m = folium.Map(location=[54.3, 60.3], zoom_start=12)

# Добавляем маркеры на карте с темпами инфляции
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f'Инфляция: {row["inflation_rate"]}%').add_to(m)

# Добавляем тепловую карту для визуализации плотности инфляции
HeatMap(data=df[['latitude', 'longitude', 'inflation_rate']], radius=15).add_to(m)

# Сохраняем карту как HTML файл
m.save("272.html")