import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты WKT для точек исхода и конца реки Шынжалы
shynzhaly_start = wkt.loads('POINT(74.123456 43.789012)')
shynzhaly_end = wkt.loads('POINT(75.123456 44.789012)')

# Создание маркеров для точек исхода и конца реки
folium.Marker([shynzhaly_start.y, shynzhaly_start.x], popup='Начало Шынжалы', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([shynzhaly_end.y, shynzhaly_end.x], popup='Конец Шынжалы', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("173.html")