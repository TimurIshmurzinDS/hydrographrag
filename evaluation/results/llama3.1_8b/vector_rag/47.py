import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), 
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {"lat": 43.1234, "lon": 76.5432},
    {"lat": 43.1245, "lon": 76.5443},
    {"lat": 43.1256, "lon": 76.5454}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup='Точка').add_to(m)

# Сохранить карту в файл
m.save("47.html")