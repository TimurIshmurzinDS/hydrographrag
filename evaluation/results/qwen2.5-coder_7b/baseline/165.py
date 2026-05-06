import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Загрузка данных о топографии и водных объектах
topography = gpd.read_file('path_to_topography_data.shp')
water_bodies = gpd.read_file('path_to_water_bodies_data.shp')

# Идентификация рек Shyzhyn и Sarykan
shyzhyn_river = water_bodies[water_bodies['name'] == 'Shyzhyn River']
sarykan_river = water_bodies[water_bodies['name'] == 'Sarykan River']

# Анализ паводков (пример: расчет площади затопленной территории)
shyzhyn_flooded_area = topography.intersection(shyzhyn_river).area.sum()
sarykan_flooded_area = topography.intersection(sarykan_river).area.sum()

print(f"Площадь затопленной территории рекой Shyzhyn: {shyzhyn_flooded_area} кв.м")
print(f"Площадь затопленной территории рекой Sarykan: {sarykan_flooded_area} кв.м")

# Визуализация результатов
m = folium.Map(location=[topography['geometry'].centroid.y.mean(), topography['geometry'].centroid.x.mean()], zoom_start=10)

folium.GeoJson(topography.to_json()).add_to(m)
folium.GeoJson(shyzhyn_river.to_json(), color='blue').add_to(m)
folium.GeoJson(sarykan_river.to_json(), color='red').add_to(m)

m.save("165.html")