import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту как GeoJson
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат рек
river_coordinates = [
    {"name": "Уржар", "coordinates": [46.7233, 78.4333]},
    {"name": "Дос (Коктал)", "coordinates": [46.7333, 79.2333]},
    {"name": "Каратал", "coordinates": [47.0333, 80.3333]}
]

# Добавление маркеров на карту для каждой реки
for river in river_coordinates:
    folium.Marker(location=river["coordinates"], popup=f"{river['name']}: {', '.join(map(str, river['coordinates']))}").add_to(m)

# Сохранение карты в файл
m.save("103.html")