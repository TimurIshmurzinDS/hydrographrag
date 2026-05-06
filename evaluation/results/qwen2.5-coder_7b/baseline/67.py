import geopandas as gpd
import folium

# Загрузка данных (предположим, что данные находятся в файле 'water_levels.geojson')
gdf = gpd.read_file('water_levels.geojson')

# Фильтрация данных по названию реки
prokhodnaya_gdf = gdf[gdf['name'] == 'Prokhodnaya River']

# Сортировка данных по дате зафиксированных уровней воды (предположим, что поле с датой называется 'date')
prokhodnaya_gdf = prokhodnaya_gdf.sort_values(by='date', ascending=False)

# Создание карты
m = folium.Map(location=[prokhodnaya_gdf.geometry.centroid.y.mean(), prokhodnaya_gdf.geometry.centroid.x.mean()], zoom_start=12)

# Добавление маркеров с уровнями воды на карте
for idx, row in prokhodnaya_gdf.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f"Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("67.html")