import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с данными о колебаниях уровня воды и городских потребностях в воде
wkt_coords = [
    {"x": -76.5, "y": 40.1},
    {"x": -77.3, "y": 39.8},
    {"x": -78.2, "y": 39.4}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['y'], coord['x']], popup=f"Уровень воды: {coord['x']}").add_to(m)

# Сохранить карту в файл
m.save("240.html")