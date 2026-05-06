import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile в геопандасе, преобразовав его в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте shapefile на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901},
    # Добавьте остальные координаты
]

# Создайте слой для координат
folium.MarkerCluster('coords').add_to(m)

for coord in wkt_coords:
    folium.CircleMarker(
        location=[coord['lat'], coord['lon']],
        radius=5,
        color='red',
        fill_color='red'
    ).add_to(folium.MarkerCluster('coords'))

# Сохраните карту в файл
m.save("251.html")