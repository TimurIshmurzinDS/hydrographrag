import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейне реки
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализировать карту Folium
m = folium.Map(location=basin_data.centroid.values[0], tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data, name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранить карту
m.save("267.html")