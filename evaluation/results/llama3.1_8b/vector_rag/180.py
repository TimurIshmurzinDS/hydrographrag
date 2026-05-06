import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о водосборе
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине водосбора и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление водосбора на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt.values.tolist(),
               name='Водосбор',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек (WKT) реки Текес
points = [
    {"location": [43.1234, 79.5678], "popup": "Река Текес"},
    {"location": [43.2345, 79.6789], "popup": "Река Сарыкан"}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point["location"], popup=point["popup"]).add_to(m)

# Сохранение карты в файл
m.save("180.html")