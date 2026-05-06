import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна реки Каскелен в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн реки Каскелен',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами (WKT)
points_wkt = [
    {"lat": 43.1234, "lon": 76.5432},
    {"lat": 43.1245, "lon": 76.5443},
    # Добавьте остальные точки в этот список
]

# Создание карты с точками
for point in points_wkt:
    folium.Marker([point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("255.html")