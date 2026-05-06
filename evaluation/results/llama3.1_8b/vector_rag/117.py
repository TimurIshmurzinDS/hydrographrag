import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка координат наблюдательных пунктов (в данном случае hardcoded)
obs_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543}
]

# Добавление наблюдательных пунктов на карту
for coord in obs_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("117.html")