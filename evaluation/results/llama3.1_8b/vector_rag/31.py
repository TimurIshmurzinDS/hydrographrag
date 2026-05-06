import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами наблюдения 0.2 км выше устья с Оской Рекой
observation_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
]

# Добавить точки на карту
for coord in observation_coords:
    folium.Marker(coord, icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("31.html")