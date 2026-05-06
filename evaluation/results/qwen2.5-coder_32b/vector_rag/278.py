import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида shapefile
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат (WKT) для демонстрации
coordinates = [
    {"name": "Region1", "wkt": "POINT(37.6173 55.7558)"},
    {"name": "Region2", "wkt": "POINT(49.1055 45.0355)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в HTML файл
m.save("278.html")