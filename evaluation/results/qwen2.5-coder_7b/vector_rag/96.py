import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=5, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание маркеров для гидрографических точек рек Уржар и Дос
urzhar_point = {"lat": 56.147, "lon": 93.817, "name": "Уржар"}
dos_point = {"lat": 55.028, "lon": 93.250, "name": "Дос"}

# Добавление маркеров на карту
folium.Marker([urzhar_point["lat"], urzhar_point["lon"]], popup=urzhar_point["name"]).add_to(m)
folium.Marker([dos_point["lat"], dos_point["lon"]], popup=dos_point["name"]).add_to(m)

# Сохранение карты
m.save("96.html")