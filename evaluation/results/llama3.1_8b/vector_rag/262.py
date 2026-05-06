import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту в виде GeoJson с зеленой заливкой и прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
                name='Бассейн',
                style_function=lambda feature: {
                    'fillColor': '#00FF00', # зеленый цвет
                    'color': '#003300',  # темно-зеленый цвет
                    'fillOpacity': 0.2    # прозрачность 20%
                }).add_to(m)

# 4. Сохранение карты в файл с именем "262.html"
m.save("262.html")