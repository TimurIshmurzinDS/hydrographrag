import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек слияния (WKT)
confluence_kishi_osak = wkt.loads('POINT(45.123456 78.910111)')
confluence_talgar = wkt.loads('POINT(45.234567 79.011122)')

# Добавление точек слияния на карту
folium.Marker([confluence_kishi_osak.y, confluence_kishi_osak.x], popup='Слияние Киши-Осек', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([confluence_talgar.y, confluence_talgar.x], popup='Слияние Талгар', icon=folium.Icon(color='blue')).add_to(m)

# Вычисление гидрологического расстояния между точками слияния
from geopy.distance import geodesic

distance = geodesic((confluence_kishi_osak.y, confluence_kishi_osak.x), (confluence_talgar.y, confluence_talgar.x)).kilometers
print(f"Гидрологическое расстояние между точками слияния: {distance:.2f} км")

# Сохранение карты
m.save("171.html")