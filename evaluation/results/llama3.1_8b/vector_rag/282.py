import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Бассейн',
               fill_color='green',
               color='darkgreen',
               fill_opacity=0.2).add_to(m)

# 4. Сохранение карты
m.save("282.html")