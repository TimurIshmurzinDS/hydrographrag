import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне Ili River
basin_data = r"data/basin_data.shp"
gdf_basin = gpd.read_file(basin_data).to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = gdf_basin.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf_basin.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат притоков (если они доступны)
prongs = [
    {'name': 'Sarykan River', 'wkt': 'POINT(74.5 41.3)'},
    {'name': 'Shynzhaly River', 'wkt': 'POINT(76.2 40.8)'}
]

# Добавление притоков на карту
for prong in prongs:
    point = wkt.loads(prong['wkt'])
    folium.Marker([point.y, point.x], popup=prong['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("156.html")