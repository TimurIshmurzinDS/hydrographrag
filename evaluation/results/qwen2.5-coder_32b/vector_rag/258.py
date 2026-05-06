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
    {"name": "Emel River", "geometry": wkt.loads("LINESTRING(76.95 43.15, 77.05 43.25)")},
    {"name": "Kumbel River", "geometry": wkt.loads("LINESTRING(78.00 43.00, 78.10 43.10)")},
    {"name": "Bayankol River", "geometry": wkt.loads("LINESTRING(79.00 42.90, 79.10 43.00)")}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson(river["geometry"], name=river["name"]).add_to(m)

# Сохранение карты в файл
m.save("258.html")