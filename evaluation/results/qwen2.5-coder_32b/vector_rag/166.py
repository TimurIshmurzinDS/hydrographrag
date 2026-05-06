import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами водного бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты folium
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты в HTML файл
m.save("166.html")