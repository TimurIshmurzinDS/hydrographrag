import pandas as pd
import geopandas as gpd
import folium

# 1. Загрузка данных о потреблении воды (замените на актуальный путь к файлу)
water_consumption = pd.read_csv("water_consumption_data.csv")

# 2. Преобразование данных в GeoDataFrame (предполагается, что данные содержат координаты)
gdf = gpd.GeoDataFrame(water_consumption, geometry=gpd.points_from_xy(water_consumption['longitude'], water_consumption['latitude']))

# 3. Создание карты с folium
m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=10)

# 4. Добавление маркеров на карту с информацией о потреблении воды
for index, row in gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Потребление: {row['water_consumption']} м3",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# 5. Сохранение карты
m.save("41.html")