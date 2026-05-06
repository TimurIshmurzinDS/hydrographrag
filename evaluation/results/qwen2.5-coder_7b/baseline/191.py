import folium
from folium.plugins import HeatMap
import pandas as pd

# Сбор данных (пример)
# Предполагаем, что у нас есть данные о текущем состоянии биоразнообразия и заборе воды
# Данные представлены в виде CSV файлов

# Загрузка данных о биоразнообразии
biodiversity_data = pd.read_csv('biodiversity_data.csv')

# Загрузка данных о заборе воды
water_extraction_data = pd.read_csv('water_extraction_data.csv')

# Создание базовой карты
m = folium.Map(location=[50.45, 30.52], zoom_start=12)

# Добавление слоя тепловых точек для биоразнообразия
HeatMap(biodiversity_data[['latitude', 'longitude', 'biodiversity_index']]).add_to(m)

# Добавление маркеров для забора воды
for index, row in water_extraction_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Water Extraction: {row['intensity']}").add_to(m)

# Сохранение карты
m.save("191.html")