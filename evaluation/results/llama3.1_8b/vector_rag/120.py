import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shape-файла
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt,
               name='Область',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами (WKT)
coordinates = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901}
]

# Добавление маркеров на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("120.html")