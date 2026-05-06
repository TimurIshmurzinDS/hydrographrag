import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными об области бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), 
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {"name": "Lepsy River", "geometry": wkt.loads("POLYGON ((40.1234 65.5678, 40.2345 65.6789, ...))")},
    {"name": "Aksu River", "geometry": wkt.loads("POLYGON ((41.3456 66.7890, 41.4567 66.8901, ...))")}
]

# Добавить координаты на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['geometry'].coords[0][1], coord['geometry'].coords[0][0]], 
                  popup=coord['name']).add_to(m)

# Сохранить карту в файл
m.save("210.html")