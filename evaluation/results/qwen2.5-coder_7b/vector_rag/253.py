import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты Альфы Центавра
alpha_centauri_coords = (44.6239, -168.8526)

# Добавление маркера для Альфы Центавра на карту
folium.Marker(alpha_centauri_coords, popup='Альфа Центавр', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("253.html")