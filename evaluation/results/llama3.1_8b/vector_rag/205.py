import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создание списка точек (если есть)
points = [
    {
        "location": [55.123, 82.456],
        "popup": "Точка 1"
    },
    {
        "location": [53.789, 81.234],
        "popup": "Точка 2"
    }
]

# 5. Добавление точек на карту
for point in points:
    folium.Marker(point["location"], popup=point["popup"]).add_to(m)

# 6. Сохранение карты
m.save("205.html")