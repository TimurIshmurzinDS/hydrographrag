import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Наблюдения высоты реки над уровнем моря (WKT)
observations = [
    {'geometry': wkt.loads('POINT(76.915833 43.225)')},
    {'geometry': wkt.loads('POINT(76.915833 43.225)')},
    {'geometry': wkt.loads('POINT(76.915833 43.225)')},
    {'geometry': wkt.loads('POINT(76.915833 43.225)')}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup='Наблюдение').add_to(m)

# Сохранение карты в файл
m.save("16.html")