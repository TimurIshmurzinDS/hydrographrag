import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с использованием raw string и преобразуйте его в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область бассейна на карту с помощью GeoJson
folium.GeoJson(gdf.to_json(), name='basin').add_child(
    folium.features.Marker(
        location=gdf.centroid.iloc[0],
        popup='Бассейн',
        icon=folium.Icon(color='green')
    )
).add_to(m)

# Создайте список словарей для координат WKT
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 44.5678, 'lon': 77.9012}
]

# Добавьте точки на карту с помощью folium.Marker
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Точка', icon=folium.Icon(color='red')).add_to(m)

# Сохраните карту в файл html
m.save("160.html")