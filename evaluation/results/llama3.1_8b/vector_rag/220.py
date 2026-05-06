import geopandas as gpd
import folium
from shapely import wkt

# Загрузка файла shapefile в GeoPandas DataFrame с преобразованием в систему координат EPSG:4326.
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты Folium с центром в середине водного бассейна и использованием слоя CartoDB positron.
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление водного бассейна на карту с прозрачностью 20%.
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).tolist(),
                name='Водный бассейн',
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты в файл.
m.save("220.html")