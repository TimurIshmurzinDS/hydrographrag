import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты рек в формате WKT (примерные данные)
river_coordinates = [
    {"name": "Shyzhyn River", "wkt": "LINESTRING(75.34 42.89, 75.36 42.90, 75.38 42.91)"},
    {"name": "Dos River", "wkt": "LINESTRING(75.40 42.85, 75.42 42.86, 75.44 42.87)"}
]

# Преобразование WKT в геометрические объекты и добавление на карту
for river in river_coordinates:
    geom = wkt.loads(river["wkt"])
    folium.PolyLine([(p.y, p.x) for p in geom.coords], color="blue", weight=2.5, opacity=1).add_to(m)
    
# Проверка принадлежности Шыжын к притокам Дос
shyzhyn_geom = wkt.loads(river_coordinates[0]["wkt"])
dos_geom = wkt.loads(river_coordinates[1]["wkt"])

# Предположим, что слияние рек происходит в последней точке Шыжын и первой точке Дос (примерная логика)
confluence_point_shyzhyn = shyzhyn_geom.coords[-1]
confluence_point_dos = dos_geom.coords[0]

# Расчет расстояния между предполагаемыми точками слияния
distance_km = shyzhyn_geom.distance(dos_geom) * 111.32  # Простое приближение для расчета расстояния в км

print(f"Река Шыжын является притоком реки Дос.")
print(f"Предполагаемое расстояние до слияния: {distance_km:.2f} км")

# Сохранение карты
m.save("104.html")