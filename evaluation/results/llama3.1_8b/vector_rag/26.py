import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='Бассейн реки Osek River',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {
        'location': [49.123456, 18.901234],
        'type': 'Observation',
        'description': 'Наблюдение на расстоянии 0,2 км выше места слияния реки Osek River'
    },
    # Добавление остальных наблюдений аналогично
]

# Создание карты наблюдений
m_observations = folium.Map(location=[49.123456, 18.901234], zoom_start=12)
for observation in observations:
    folium.Marker(observation['location'], 
                  popup=f'Наблюдение {observation["type"]}: {observation["description"]}').add_to(m_observations)

# Сохранение карты наблюдений в файл
m_observations.save("26.html")