import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создание списка точек с координатами (WKT)
points = [
    {
        "name": "Река Аягоз",
        "geometry": wkt.loads("POINT(47.0833 78.2833)"),
        "properties": {"description": "Река Аягоз"}
    },
    {
        "name": "Город Аягоз",
        "geometry": wkt.loads("POINT(47.1333 78.3333)"),
        "properties": {"description": "Город Аягоз"}
    }
]

# 5. Добавление точек на карту
for point in points:
    folium.Marker(point['geometry'], 
                  popup=point['name'] + ": " + point['properties']['description'],
                  icon=folium.Icon(color='red')).add_to(m)

# 6. Сохранение карты в файл
m.save("228.html")