import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейнах из shapefile
basins = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализировать карту Folium с центром в центре basins
m = folium.Map(location=basins.centroid.values[0], tiles='CartoDB positron')

# Добавить basins на карту
folium.GeoJson(data=basins, name="Basins", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранить карту в HTML-файл
m.save("177.html")