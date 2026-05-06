import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с границами бассейна реки Кумбель
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium, центрированную на геометрическом центре бассейна
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Добавить границу бассейна на карту
folium.GeoJson(basin.geometry.values[0], name="Бассейн реки Кумбель", 
               fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Сохранить карту в HTML-файл
m.save("243.html")