import pandas as pd
import geopandas as gpd
import folium

# Загрузка данных о потреблении воды (пример)
water_consumption_data = pd.read_csv('water_consumption.csv')

# Пример данных:
# water_consumption_data.head()

# Загрузка географических данных фермерских хозяйств (пример)
farm_locations = gpd.read_file('farm_locations.shp')

# Пример данных:
# farm_locations.head()

# Объединение данных по потреблению воды и координатам фермерских хозяйств
merged_data = pd.merge(water_consumption_data, farm_locations, left_on='farm_id', right_on='id')

# Создание карты
m = folium.Map(location=[43.0522, 76.918], zoom_start=10)

# Добавление маркеров с потреблением воды на фермерских хозяйствах
for idx, row in merged_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Фермерское хозяйство: {row['farm_name']}<br>Потребление воды: {row['water_consumption']} м³",
        icon=folium.Icon(color='blue', icon='drop')
    ).add_to(m)

# Сохранение карты
m.save("41.html")