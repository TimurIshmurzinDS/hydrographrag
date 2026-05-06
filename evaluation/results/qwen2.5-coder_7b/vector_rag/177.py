import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах
basin_data = r"data/basin_data.shp"
gdf = gpd.read_file(basin_data)
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в геометрии бассейна
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание маркеров для точек впадин (если есть)
confluences = [
    {"name": "Осетинский", "wkt": "POINT(45.1234 46.7890)"},
    {"name": "Коксун", "wkt": "POINT(47.1234 48.7890)"},
    {"name": "Байкал", "wkt": "POINT(49.1234 50.7890)"}
]

for confluence in confluences:
    point = wkt.loads(confluence["wkt"])
    folium.Marker([point.y, point.x], popup=confluence["name"]).add_to(m)

# Сохранение карты
m.save("177.html")