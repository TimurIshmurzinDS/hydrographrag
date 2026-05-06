import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты Folium
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты рек (WKT)
rivers = [
    {"name": "Sarykan River", "geometry": wkt.loads("LINESTRING(76.95 43.1, 77.0 43.2)"), "discharge": 15},
    {"name": "Tekeli River", "geometry": wkt.loads("LINESTRING(76.85 43.15, 76.9 43.25)"), "discharge": 20}
]

# Добавление рек на карту
for river in rivers:
    folium.PolyLine(locations=[list(coord) for coord in list(river['geometry'].coords)], color='blue', weight=2.5, popup=f"{river['name']}, Расход: {river['discharge']} м³/с").add_to(m)

# Сохранение карты
m.save("110.html")