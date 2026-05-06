import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат рек (WKT)
river_coords = [
    {'name': 'Улькен Алматы', 'wkt': 'POINT(76.915833 43.225)', 'type': 'HY_HydroFeature'},
    {'name': 'Емель', 'wkt': 'POINT(76.900000 43.230000)', 'type': 'HY_HydroFeature'},
    {'name': 'Тентек', 'wkt': 'POINT(76.850000 43.210000)', 'type': 'HY_HydroFeature'}
]

# Преобразование WKT в GeoDataFrame
river_gdf = gpd.GeoDataFrame(river_coords, geometry=[wkt.loads(coord['wkt']) for coord in river_coords])
river_gdf = river_gdf.to_crs('EPSG:4326')

# Добавление рек на карту
for idx, row in river_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Сохранение карты
m.save("105.html")