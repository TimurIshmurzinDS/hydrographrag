import pandas as pd
import geopandas as gpd
import folium

# Загрузка данных о датчиках уровня воды
data = {
    'river': ['Osek', 'Osek', 'Koktal', 'Koktal'],
    'latitude': [50.123, 50.456, 51.789, 52.012],
    'longitude': [18.345, 18.678, 19.012, 19.345],
    'water_level': [1.2, 1.5, 2.0, 2.5]
}

df = pd.DataFrame(data)

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Создание карты
m = folium.Map(location=[50.834, 19.067], zoom_start=10)

# Добавление маркеров с уровнями воды
for idx, row in gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}<br>Уровень воды: {row['water_level']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("73.html")