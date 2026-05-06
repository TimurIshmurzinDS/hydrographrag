import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Уржар
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат притоков (WKT)
tributaries = [
    {"name": "Узын Каргалы", "geometry": wkt.loads("LINESTRING(76.95 43.1, 77.0 43.2)")}
]

# Добавление притоков на карту
for tributary in tributaries:
    folium.GeoJson(
        gpd.GeoSeries([tributary["geometry"]], crs='EPSG:4326'),
        style_function=lambda x: {'color': 'blue', 'weight': 2}
    ).add_to(m)

# Сохранение карты
m.save("91.html")