import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
coordinates = [
    {"name": "Уржар", "wkt": "LINESTRING(51.3486 51.9765, 51.3502 51.9778)"},
    {"name": "Безы", "wkt": "LINESTRING(51.3456 51.9735, 51.3472 51.9748)"}
]

# Добавление линий рек на карту
for coord in coordinates:
    line = wkt.loads(coord["wkt"])
    folium.PolyLine(locations=list(zip(*line.xy)), color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в HTML файл
m.save("199.html")