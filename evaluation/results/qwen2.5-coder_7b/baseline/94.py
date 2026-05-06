import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о реках Тентек и Быж (пример использования Shapefile)
tentek_gdf = gpd.read_file('path_to_tentek_shapefile.shp')
byzh_gdf = gpd.read_file('path_to_byzh_shapefile.shp')

# Определение верхнего течения реки Тентек
def find_highest_point(line):
    return line.coords[np.argmax([point[1] for point in line.coords])]

tentek_line = tentek_gdf.geometry.iloc[0]
highest_point_tentek = find_highest_point(tentek_line)

# Определение верхнего течения реки Быж
byzh_line = byzh_gdf.geometry.iloc[0]
highest_point_byzh = find_highest_point(byzh_line)

# Визуализация на карте
m = folium.Map(location=[(tentek_line.centroid.y + byzh_line.centroid.y) / 2, (tentek_line.centroid.x + byzh_line.centroid.x) / 2], zoom_start=10)

folium.Marker([highest_point_tentek[1], highest_point_tentek[0]], popup='Верхнее течение реки Тентек', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([highest_point_byzh[1], highest_point_byzh[0]], popup='Верхнее течение реки Быж', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("94.html")