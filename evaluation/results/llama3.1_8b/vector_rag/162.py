import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине области
centroid = basin_data.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(data=basin_data.to_crs(epsg=4326).json,
               name='Область',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с данными о снеготаянии и паводках
points_data = [
    {
        'location': [48.1234, 87.5678],
        'snow_melt': 10,
        'floods': 5
    },
    {
        'location': [48.2345, 88.9012],
        'snow_melt': 20,
        'floods': 10
    }
]

# Добавление точек на карту
for point in points_data:
    folium.Marker(point['location'], popup=f'Снеготаяние: {point["snow_melt"]}, Паводки: {point["floods"]}').add_to(m)

# Сохранение карты в файл
m.save("162.html")