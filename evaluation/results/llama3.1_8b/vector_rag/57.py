import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
coordinates = [
    {
        "lat": 55.123456,
        "lon": 37.654321
    },
    {
        "lat": 56.789012,
        "lon": 38.901234
    }
]

# Создание карты с маркерами на координатах (WKT)
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup=f'Координаты: {coord["lat"]}, {coord["lon"]}').add_to(m)

# Сохранение карты в файл
m.save("57.html")