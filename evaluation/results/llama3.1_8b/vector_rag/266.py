import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту как GeoJson с зеленой заливкой
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), name='basin').add_to(m)
folium.Marker([46.5, 76.0], icon=folium.Icon(color='red')).add_to(m)

# Создание списка координат полей (в данном случае hardcoded)
fields_coords = [
    {'lat': 46.5231, 'lon': 76.0232},
    {'lat': 46.5253, 'lon': 76.0254},
    {'lat': 46.5275, 'lon': 76.0276}
]

# Добавление полей на карту как маркеры
for field in fields_coords:
    folium.Marker([field['lat'], field['lon']], icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты в файл
m.save("266.html")