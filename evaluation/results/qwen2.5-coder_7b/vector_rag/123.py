import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из контекста
kurty_river = {
    "name": "Kurty River",
    "geometry": wkt.loads("LINESTRING(45.123 78.901, 46.234 79.012, 47.345 79.123)")
}

sharyn_river = {
    "name": "Sharyn River",
    "geometry": wkt.loads("LINESTRING(48.456 80.123, 49.567 81.234, 50.678 82.345)")
}

# Создание GeoDataFrame для рек
rivers_gdf = gpd.GeoDataFrame([kurty_river, sharyn_river], crs='EPSG:4326')

# Загрузка границы бассейна из shapefile (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs('EPSG:4326', inplace=True)

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление рек на карту
for _, row in rivers_gdf.iterrows():
    folium.PolyLine(row['geometry'].coords, color='blue', weight=2).add_to(m)

# Сохранение карты
m.save("123.html")