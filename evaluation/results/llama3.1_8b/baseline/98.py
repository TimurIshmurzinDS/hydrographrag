import folium

# Загрузить данные о реках из GeoNames
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Создать карту
m = folium.Map(location=[55.0, 82.0], zoom_start=6)

# Данные о реке Тентек
tenteck_data = {
    'name': 'Тентек',
    'geometry': gpd.GeoSeries.from_wkt('POLYGON ((82.5 54.9, 83.1 55.2, 83.4 54.8, 82.5 54.9))')
}

# Данные о реке Быж
byzh_data = {
    'name': 'Быж',
    'geometry': gpd.GeoSeries.from_wkt('POLYGON ((81.0 53.2, 81.4 52.8, 80.6 53.1, 81.0 53.2))')
}

# Добавить слои для рек на карту
folium.GeoJson(tenteck_data['geometry'].to_json(), name='Тентек').add_to(m)
folium.GeoJson(byzh_data['geometry'].to_json(), name='Быж').add_to(m)

# Определить бассейны рек
def get_basin(geometry):
    # Для простоты, предположим, что бассейн определяется как область с координатами (82.5 54.9)
    return gpd.GeoSeries.from_wkt('POLYGON ((82.5 54.9, 83.1 55.2, 83.4 54.8, 82.5 54.9))')

# Добавить информацию о бассейнах на карту
for river in [tenteck_data['geometry'], byzh_data['geometry']]:
    folium.Marker(river.centroid, popup=f'Бассейн: {get_basin(river).name}').add_to(m)

# Сохранить карту в файл
m.save("98.html")