import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейне
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализировать карту folium
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Добавить границы бассейна на карту
folium.GeoJson(basin, name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранить карту
m.save("73.html")