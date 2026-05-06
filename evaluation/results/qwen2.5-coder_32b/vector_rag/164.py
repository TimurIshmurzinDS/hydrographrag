import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), добавляем их на карту
coordinates = [
    {"name": "Ili River", "wkt": "POINT(87.6543 49.1234)"},
    {"name": "Shynzhaly River", "wkt": "POINT(87.7890 49.2345)"}
]

for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты
m.save("164.html")