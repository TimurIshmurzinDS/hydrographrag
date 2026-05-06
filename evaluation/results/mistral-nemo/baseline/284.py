import pandas as pd
import geopandas as gpd
import folium

# Загрузите данные о климатических изменениях на Марсе
data = pd.read_csv('mars_climate_data.csv')

# Преобразование данных в формат GeoDataFrame с помощью географических координат (долгота и широта)
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))

# Анализ исторических изменений климата
# Например, средняя температура за каждый год
avg_temperature = data.groupby('year')['temperature'].mean()

# Создание карты Марса с помощью folium
m = folium.Map(location=[0, 0], zoom_start=3)

# Добавление маркеров на карту для каждой точки данных о климатических изменениях
for index, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Температура: {row["temperature"]}°C\nДавление: {row["pressure"]} Па\nВетер: {row["wind_speed"]} м/с').add_to(m)

# Сохранение финальной карты как "284.html"
m.save("284.html")