import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о водоемах в системе координат EPSG:4326
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине области и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту с прозрачностью 20%
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Область',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами реки Караой (в данном случае hardcoded)
karaoy_coords = [
    {"lat": 43.1234, "lon": 77.5678},
    {"lat": 43.2345, "lon": 78.6789}
]

# Добавление маркеров на карту для реки Караой
for coord in karaoy_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Река Караой').add_to(m)

# Сохранение карты в файл с именем "224.html"
m.save("224.html")