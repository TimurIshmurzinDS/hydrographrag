import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Аксу
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты Folium
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Добавление бассейна реки на карту
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Сохранение карты
m.save("237.html")