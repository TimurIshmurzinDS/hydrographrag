import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту как GeoJSON
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT) для добавления на карту
coordinates = [
    {
        'lat': 55.123456,
        'lon': 37.654321,
        'name': 'Наблюдение 1'
    },
    {
        'lat': 55.987654,
        'lon': 38.765432,
        'name': 'Наблюдение 2'
    }
]

# Добавить координаты на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup=coord['name']).add_to(m)

# Сохранить карту в файл
m.save("14.html")