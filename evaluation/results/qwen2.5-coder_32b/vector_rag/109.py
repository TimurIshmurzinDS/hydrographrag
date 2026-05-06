import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты рек (примерные, для демонстрации)
rivers = [
    {"name": "Byzhy River", "geometry": wkt.loads("LINESTRING(75.34 48.12, 75.40 48.15)")},
    {"name": "Lepsy River", "geometry": wkt.loads("LINESTRING(75.28 48.10, 75.32 48.13)")}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson(gpd.GeoSeries(river["geometry"]).to_json(), name=river["name"], style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("109.html")