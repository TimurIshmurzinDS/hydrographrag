import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка точек наблюдения (в данном случае hardcoded)
points_of_interest = [
    {
        'name': 'Пункт наблюдения на реке Kishi Osek River',
        'location': [43.123456, 76.789012],
        'description': 'Расположен в 1,7 км выше устья'
    }
]

# Добавление точек наблюдения на карту
for point in points_of_interest:
    folium.Marker(point['location'], popup=point['name'] + ': ' + point['description']).add_to(m)

# Создание списка значений уровня воды (в данном случае hardcoded)
water_level_values = [
    {
        'date': '2022-01-01',
        'value': 10.5
    },
    {
        'date': '2022-02-01',
        'value': 12.8
    }
]

# Добавление значений уровня воды на карту
for value in water_level_values:
    folium.Marker([43.123456, 76.789012], popup=value['date'] + ': ' + str(value['value']) + ' м').add_to(m)

# Сохранение карты в файл
m.save("122.html")