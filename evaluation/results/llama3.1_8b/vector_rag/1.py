import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в системе координат EPSG:4326
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту как GeoJSON с зеленой заливкой и темно-зеленой линией
folium.GeoJson(basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Создать список словарей для координат (WKT) наблюдений
wkt_coords = [
    {'lat': 43.1234, 'lon': 87.5678},
    {'lat': 42.9012, 'lon': 88.3456}
]

# Добавить точки на карту с использованием координат (WKT)
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Добавить значение уровня воды в реке Или
water_level_value = 10.5  # Значение уровня воды (Water_level_Value)
folium.Marker([43.1234, 87.5678], popup=f'Уровень воды: {water_level_value} м').add_to(m)

# Сохранить карту в файл html
m.save("1.html")