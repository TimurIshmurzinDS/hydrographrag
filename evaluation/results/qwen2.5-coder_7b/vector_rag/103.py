import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты рек в формате WKT
coordinates = {
    "Уржар Река": "LINESTRING(76.953148 43.22361, 76.953148 43.22361)",
    "Дос Река": "LINESTRING(76.953148 43.22361, 76.953148 43.22361)",
    "Каратал Река": "LINESTRING(76.953148 43.22361, 76.953148 43.22361)"
}

# Добавление рек на карту
for name, wkt_str in coordinates.items():
    geom = wkt.loads(wkt_str)
    folium.GeoJson(geom, style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("103.html")