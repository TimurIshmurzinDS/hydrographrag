import geopandas as gpd
import folium

# Предположим, что у нас есть GeoDataFrame с данными о реках
# Для примера создадим его вручную
data = {
    'name': ['Karaoy River', 'Baskan River', 'Temirlik River', 'Another River'],
    'geometry': [
        'LINESTRING (30 40, 31 41)',
        'LINESTRING (32 42, 33 43)',
        'LINESTRING (34 44, 35 45)',
        'LINESTRING (36 46, 37 47)'
    ]
}
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Фильтрация рек по списку
rivers_of_interest = ['Karaoy River', 'Baskan River', 'Temirlik River']
filtered_gdf = gdf[gdf['name'].isin(rivers_of_interest)]

# Предположим, что у нас есть данные о риске затопления для каждой реки
flood_risk_data = {
    'Karaoy River': 'Высокий',
    'Baskan River': 'Средний',
    'Temirlik River': 'Низкий'
}

# Создание карты с помощью folium
m = folium.Map(location=[42, 35], zoom_start=8)

# Добавление маркеров для выбранных рек и отображение информации о риске затопления
for _, row in filtered_gdf.iterrows():
    name = row['name']
    coords = row['geometry'].centroid.coords[0]
    flood_risk = flood_risk_data.get(name, 'Неизвестно')
    folium.Marker(
        location=coords,
        popup=f"Река: {name}<br>Текущий риск затопления: {flood_risk}",
        icon=folium.Icon(color='red' if flood_risk == 'Высокий' else ('orange' if flood_risk == 'Средний' else 'green'))
    ).add_to(m)

# Сохранение карты в файл
m.save("90.html")