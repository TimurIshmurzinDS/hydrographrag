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

# Если есть координаты (WKT), добавляем их на карту
coordinates = [
    {"name": "Shyzhyn River", "wkt": "LINESTRING(76.95 43.1, 77.0 43.2)"},
    {"name": "Sarykan River", "wkt": "LINESTRING(76.85 43.15, 76.9 43.25)"}
]

for coord in coordinates:
    geom = wkt.loads(coord["wkt"])
    folium.GeoJson(gpd.GeoSeries([geom], crs='EPSG:4326').to_json(), name=coord["name"], style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты
m.save("165.html")