import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание интерактивной карты с центром в середине области
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 48.1234, 'lon': 36.5678},
    {'lat': 47.9012, 'lon': 37.3456}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("272.html")