import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создать список точек пересечения водоразделов
points = [
    {'lat': 54.1234, 'lon': 23.4567},
    {'lat': 54.7890, 'lon': 24.3210}
]

# Добавить точки на карту
for point in points:
    folium.Marker(point).add_to(m)

# Сохранить карту в файл
m.save("174.html")