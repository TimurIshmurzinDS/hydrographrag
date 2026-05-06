import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные об области бассейна из файла data/basin_data.shp и преобразовать в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data\bassin_data.shp").to_crs('EPSG:4326')

# Создать карту с использованием центроида области бассейна и добавить на неё область бассейна в виде зеленого полигона
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)
folium.Marker([55.7558, 37.6173], popup='Бызж').add_to(m)

# Если в контексте содержатся координаты (WKT), создать список словарей для отображения точек на карте
wkt_coords = [
    {'lat': 55.7558, 'lon': 37.6173},
    # Добавьте сюда остальные точки из WKT
]

# Создать маркеры для точек
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Точка').add_to(m)

# Сохранить карту в файл
m.save("191.html")