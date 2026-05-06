import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о границах бассейна
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализировать карту Folium
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin, name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранить карту
m.save("270.html")