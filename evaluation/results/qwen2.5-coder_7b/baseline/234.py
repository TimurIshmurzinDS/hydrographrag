import folium
import pandas as pd
import geopandas as gpd

# Загрузка данных о реке Шарын (пример: GeoJSON)
sharyn_data = gpd.read_file('path_to_sharyn_data.geojson')

# Создание базовой карты
m = folium.Map(location=[43.0, 76.0], zoom_start=12)

# Добавление слоя с данными о реке Шарын
folium.GeoJson(sharyn_data).add_to(m)

# Загрузка данных о сезонных разливах (пример: CSV)
diversions_data = pd.read_csv('path_to_diversions_data.csv')

# Добавление маркеров для сезонных разливов
for index, row in diversions_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Разлив {row['diversion_name']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("234.html")