import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание hardcoded списка точек для демонстрации расчета
points = [
    {"lat": 43.123456, "lon": 76.789012},
    {"lat": 43.234567, "lon": 77.890123}
]

# Добавление точек на карту
for point in points:
    folium.Marker([point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("171.html")