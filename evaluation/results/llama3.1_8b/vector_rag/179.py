import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузить shapefile бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# 2. Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# 3. Добавить бассейн на карту
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создать список наблюдательных пунктов
observation_points = [
    {'lat': 55.123456, 'lon': 37.654321},
    {'lat': 55.234567, 'lon': 38.765432},
    {'lat': 55.345678, 'lon': 39.876543},
    {'lat': 55.456789, 'lon': 40.987654}
]

# 5. Добавить наблюдательные пункты на карту
for point in observation_points:
    folium.Marker(point['lat'], point['lon']).add_to(m)

# 6. Сохранить карту в файл
m.save("179.html")