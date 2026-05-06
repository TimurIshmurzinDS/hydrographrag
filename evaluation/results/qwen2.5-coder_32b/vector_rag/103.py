import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs(epsg=4326)

# Инициализация карты с центром, соответствующим центроиду бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты рек в формате WKT (примерные данные)
river_coordinates = [
    {"name": "Уржар Река", "coordinates": wkt.loads("LINESTRING(76.95 43.2, 77.05 43.3, 77.15 43.4)")},
    {"name": "Дос Река", "coordinates": wkt.loads("LINESTRING(76.85 43.1, 76.95 43.2, 77.05 43.3)")},
    {"name": "Каратал Река", "coordinates": wkt.loads("LINESTRING(77.05 43.4, 77.15 43.5, 77.25 43.6)")}
]

# Добавление маршрутов рек на карту
for river in river_coordinates:
    folium.PolyLine(locations=list(zip(river['coordinates'].coords.y, river['coordinates'].coords.x)), color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("103.html")