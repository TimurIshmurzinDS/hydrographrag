import geopandas as gpd
from shapely.geometry import shape
import folium

# Подготовка данных
river_data = {
    'geometry': [
        shape('POLYGON ((-122.0 37.0, -121.0 37.0, -121.0 38.0, -122.0 38.0, -122.0 37.0))'), 
        shape('POLYGON ((-123.0 36.0, -122.0 36.0, -122.0 37.0, -123.0 37.0, -123.0 36.0))')
    ],
    'name': ['Текес', 'Приток Текеса']
}

river_gdf = gpd.GeoDataFrame(river_data, geometry='geometry')

# Создание топологической модели
river_gdf['length'] = river_gdf.length()
river_gdf['area'] = river_gdf.area()

# Оценка плотности дренажной сети
density = (river_gdf['length'].sum() / river_gdf['area'].sum()) * 100

print(f'Плотность дренажной сети в бассейне реки Текес: {density:.2f}%')

# Визуализация на карте
m = folium.Map(location=[37.0, -122.0], zoom_start=10)
folium.GeoJson(river_gdf.to_json()).add_to(m)

# Сохранение карты в файл
m.save("172.html")