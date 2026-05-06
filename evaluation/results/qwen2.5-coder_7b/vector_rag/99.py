import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат истоков рек (если они были бы известны)
# Пример:
# source_points = [
#     {"name": "Исток Улькен Алматы", "wkt": "POINT(76.915 43.208)"},
#     {"name": "Исток Уржар", "wkt": "POINT(76.920 43.210)"}
# ]

# Если координаты известны, добавление точек на карту
# for point in source_points:
#     folium.Marker([point['wkt'].xy[1][0], point['wkt'].xy[0][0]], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("99.html")