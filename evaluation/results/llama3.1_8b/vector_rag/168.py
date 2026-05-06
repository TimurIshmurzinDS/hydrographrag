import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).tolist(),
               name='Бассейн реки Эмель',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек для реки Сарыкан
points_sarykan = [
    {
        'location': [55.123456, 82.654321],
        'popup': 'Река Сарыкан',
        'icon': folium.Icon(color='blue')
    }
]

# Добавление точек на карту
for point in points_sarykan:
    folium.Marker(point['location'], popup=point['popup'], icon=point['icon']).add_to(m)

# Сохранение карты в файл
m.save("168.html")