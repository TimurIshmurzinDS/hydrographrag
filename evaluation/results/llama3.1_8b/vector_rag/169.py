import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами русел рек Шынжалы и Талгар (предположительно)
river_coords = [
    {"type": "Feature", "geometry": wkt.loads("LINESTRING(77.1234 42.5678, 77.2345 42.6789)")},
    {"type": "Feature", "geometry": wkt.loads("LINESTRING(78.9012 43.1111, 79.0123 43.2222)")},
]

# Добавление русел рек на карту
folium.GeoJson(river_coords,
               name='Русла рек',
               style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.1}).add_to(m)

# Сохранение карты в файл
m.save("169.html")