import folium
from geopandas import GeoDataFrame
from shapely.geometry import Point

# Пример данных (замените на реальные данные)
data = {
    'geometry': [Point(10.5, 48.2), Point(10.6, 48.3)],
    'crop_type': ['Wheat', 'Corn'],
    'area': [100, 150],
    'climate_score': [8, 7],
    'infrastructure_score': [9, 8]
}

# Создание GeoDataFrame
gdf = GeoDataFrame(data, geometry='geometry')

# Создание карты
m = folium.Map(location=[48.25, 10.55], zoom_start=13)

# Добавление маркеров на карте
for idx, row in gdf.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f"Участок {idx + 1}: Тип культуры - {row['crop_type']}, Площадь - {row['area']} га",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Сохранение карты
m.save("268.html")