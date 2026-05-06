import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные об области бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине области бассейна
centroid = basin_data.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавить область бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.__geo_interface__,
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если имеются координаты (WKT), создать список словарей для визуализации результатов на карте
if hasattr(basin_data, 'geometry'):
    wkt_coords = basin_data.geometry.apply(lambda x: {'type': 'Point', 'coordinates': [x.x, x.y]})
else:
    wkt_coords = []

# Сохранить карту в файл
m.save("285.html")