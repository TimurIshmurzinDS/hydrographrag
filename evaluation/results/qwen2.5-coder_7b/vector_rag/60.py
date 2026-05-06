import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Karkara River и уровнях воды
karkara_river_data = {
    'Date': ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01'],
    'Water_level_Value': [10, 12, 15, 17, 20]
}

# Загрузка данных о осадках
precipitation_data = {
    'Date': ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01'],
    'Precipitation': [5, 7, 10, 12, 15]
}

# Преобразование данных в DataFrame
karkara_river_df = pd.DataFrame(karkara_river_data)
precipitation_df = pd.DataFrame(precipitation_data)

# Объединение данных по дате
merged_data = pd.merge(karkara_river_df, precipitation_df, on='Date')

# Создание карты
m = folium.Map(location=[39.0456, 32.8719], zoom_start=10, tiles='CartoDB positron')

# Добавление реки Karkara River на карту
karkara_river_gdf = gpd.GeoDataFrame({'geometry': [wkt.loads('POLYGON((32.865 39.045, 32.875 39.045, 32.875 39.055, 32.865 39.055, 32.865 39.045))')], 'name': 'Karkara River'})
karkara_river_gdf.crs = 'EPSG:4326'
folium.GeoJson(karkara_river_gdf.to_json(), style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Добавление точек с уровнями воды и осадками на карту
for index, row in merged_data.iterrows():
    folium.Marker([39.0456, 32.8719], popup=f"Water Level: {row['Water_level_Value']} m<br>Precipitation: {row['Precipitation']} mm").add_to(m)

# Сохранение карты
m.save("60.html")