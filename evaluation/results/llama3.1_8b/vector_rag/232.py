import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с центром в координатах центра бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление данных о бассейне на карту в виде GeoJson с зеленой заливкой и прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
                name='Бассейн',
                style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Сохранение карты в файл с именем "232.html"
m.save("232.html")