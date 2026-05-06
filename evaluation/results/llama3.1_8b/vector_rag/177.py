import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейнах
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), name='bassins').add_to(m)

# Создание списка точек наблюдения (в данном случае hardcoded)
points = [
    {'lat': 55.123, 'lon': 36.456},
    {'lat': 54.789, 'lon': 37.321}
]

# Добавление точек наблюдения на карту
for point in points:
    folium.Marker([point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("177.html")