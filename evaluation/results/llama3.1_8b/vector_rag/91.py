import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), name='bass').add_to(m)

# Создание списка координат притоков реки Уржар (в данном случае только река Узен Кагалы)
pritoki = [
    {
        'name': 'Узен Кагалы',
        'coordinates': wkt.loads('POINT(47.123 69.456)').coords[:2]
    }
]

# Создание карты с координатами притоков
for i, pritok in enumerate(pritoki):
    folium.Marker(location=pritok['coordinates'], popup=pritok['name']).add_to(m)

# Сохранение карты в файл
m.save("91.html")