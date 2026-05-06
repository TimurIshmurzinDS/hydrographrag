import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассее
basin_data = r"data/basin_data.shp"
gdf_basin = gpd.read_file(basin_data)
gdf_basin = gdf_basin.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассеина
centroid = gdf_basin.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассеина на карту
folium.GeoJson(gdf_basin.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Сохранение карты
m.save("259.html")