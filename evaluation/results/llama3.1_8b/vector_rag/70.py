import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузить shapefile с данными бассейна в системе координат EPSG:4326.
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# 2. Создать карту Folium с центром в середине бассейна и использовать плитки CartoDB positron.
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# 3. Добавить данные бассейна на карту как GeoJSON с зеленой заливкой и темно-зеленым контуром.
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создать список словарей для координат наблюдений (WKT).
wkt_coords = [
    {"lat": 43.123, "lon": 76.456},
    {"lat": 43.234, "lon": 76.567},
    {"lat": 43.345, "lon": 76.678}
]

# 5. Добавить точки наблюдений на карту.
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# 6. Сохранить карту в файл с именем "70.html".
m.save("70.html")