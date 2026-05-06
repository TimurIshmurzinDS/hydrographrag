import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в координатах центра бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Добавление бассейна на карту в виде GeoJson с зеленой заливкой и прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
                name='Бассейн',
                style_function=lambda feature: {
                    'fillColor': 'green',
                    'color': 'darkgreen',
                    'fillOpacity': 0.2
                }).add_to(m)

# Создание списка словарей для координат (WKT)
coordinates = [
    {'lat': basin_data.centroid.y, 'lon': basin_data.centroid.x},
]

# Добавление маркеров на карту с координатами
for coordinate in coordinates:
    folium.Marker([coordinate['lat'], coordinate['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл html
m.save("140.html")