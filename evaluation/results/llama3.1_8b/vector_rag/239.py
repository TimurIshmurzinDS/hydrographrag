import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shape-файла в геопандас
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).tolist(),
               name='Область',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек для отображения на карте
points = [
    {
        'location': [46.1234, 68.9012],
        'popup': 'Наблюдение 0.2 км выше устья Оск Река'
    }
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['location'], popup=point['popup']).add_to(m)

# Сохранение карты в файл
m.save("239.html")