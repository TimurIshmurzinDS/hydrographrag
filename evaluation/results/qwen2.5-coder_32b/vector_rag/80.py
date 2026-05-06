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

# Пример координат рек (WKT) - заменить на реальные данные
coordinates = [
    {"name": "Tokyraun River", "wkt": "LINESTRING(75.9184 43.0622, 75.9284 43.0722)"},
    {"name": "Koktal River", "wkt": "LINESTRING(75.8184 43.1622, 75.8284 43.1722)"}
]

# Добавление рек на карту
for coord in coordinates:
    line = wkt.loads(coord["wkt"])
    folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=2.5, opacity=1).add_to(m)
    folium.Marker(location=[line.centroid.y, line.centroid.x], popup=coord["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("80.html")