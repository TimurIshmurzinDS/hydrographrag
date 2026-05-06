import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о реках Тентек и Быж (пример данных)
tentek = gpd.GeoDataFrame({'name': ['Тентек'], 'geometry': [LineString([(10, 20), (30, 40)])]})
byzh = gpd.GeoDataFrame({'name': ['Быж'], 'geometry': [LineString([(50, 60), (70, 80)])]})

# Загрузка данных о бассейнах (пример данных)
basins = gpd.read_file('path_to_basins_shapefile.shp')

# Определение бассейнов для каждой реки
tentek['basin'] = tentek.geometry.apply(lambda geom: basins[basins.intersects(geom)].iloc[0]['name'])
byzh['basin'] = byzh.geometry.apply(lambda geom: basins[basins.intersects(geom)].iloc[0]['name'])

# Визуализация результатов
m = folium.Map(location=[45, 30], zoom_start=6)

folium.GeoJson(tentek.to_json(), name='Tentek').add_to(m)
folium.GeoJson(byzh.to_json(), name='Byzh').add_to(m)
folium.GeoJson(basins.to_json(), name='Basins', style_function=lambda x: {'color': 'blue'}).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("98.html")