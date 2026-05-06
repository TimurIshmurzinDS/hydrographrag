import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='basin',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат (WKT) для реки Токыраун
river_coords = [
    {"type": "Point", "coordinates": [55.123, 37.456]},
    {"type": "Point", "coordinates": [54.789, 36.321]}
]

# Создание карты с координатами (WKT) реки Токыраун
m.add_child(folium.Marker(location=[river_coords[0]["coordinates"][1], river_coords[0]["coordinates"][0]], 
                          popup="Река Токыраун",
                          icon=folium.Icon(color='blue')))

# Сохранение карты в файл
m.save("193.html")