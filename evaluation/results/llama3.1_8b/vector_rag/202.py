import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами (WKT) рек
coordinates = [
    {"name": "Emel River", "wkt": wkt.loads("POLYGON ((...))")},
    {"name": "Turgen River", "wkt": wkt.loads("POLYGON ((...))")}
]

# Добавление маркеров на карту для каждой реки
for river in coordinates:
    folium.Marker(location=[river["wkt"].centroid.y, river["wkt"].centroid.x], 
                  popup=river["name"]).add_to(m)

# Сохранение карты в файл
m.save("202.html")