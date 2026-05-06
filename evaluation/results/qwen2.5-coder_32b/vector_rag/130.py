import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из файла shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Баянколь
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат стока реки Баянколь и базового уровня реки Шилик (WKT)
coordinates = [
    {"name": "Bayankol River Outfall", "wkt": "POINT(100.5 45.3)"},
    {"name": "Shilik River Base Level", "wkt": "POINT(100.7 45.2)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("130.html")