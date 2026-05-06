import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile с использованием raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 44.5678, 'lon': 77.9012}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup='Наблюдение').add_to(m)

# Сохранение карты в файл с именем '9.html'
m.save("9.html")