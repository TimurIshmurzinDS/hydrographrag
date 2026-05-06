import folium
from shapely.geometry import Polygon, Point
import geopandas as gpd

# Пример данных о местоположении реки Аксу и его бассейна (замените на реальные данные)
river_geometry = Polygon([(105.0, 43.0), (106.0, 43.0), (106.0, 44.0), (105.0, 44.0)])
basin_geometry = Polygon([(104.0, 42.0), (107.0, 42.0), (107.0, 45.0), (104.0, 45.0)])

# Создаем GeoDataFrame для реки и бассейна
river_gdf = gpd.GeoDataFrame({'name': 'Аксу', 'geometry': [river_geometry]})
basin_gdf = gpd.GeoDataFrame({'name': 'Бассейн Аксу', 'geometry': [basin_geometry]})

# Пример данных о высоте воды и площади бассейна (замените на реальные данные)
water_level_data = {
    'date': ['2021-07-01', '2021-08-01', '2021-09-01'],
    'height': [5.0, 6.0, 7.0]
}

# Пример данных о вероятности наводнения (замените на реальные данные)
flood_probability_data = {
    'date': ['2021-07-01', '2021-08-01', '2021-09-01'],
    'probability': [0.1, 0.3, 0.5]
}

# Создаем GeoDataFrame для вероятности наводнения
flood_probability_gdf = gpd.GeoDataFrame(flood_probability_data)

# Визуализация на карте с использованием folium
m = folium.Map(location=[43.5, 106.0], zoom_start=8)

folium.GeoJson(river_gdf.to_json(), name='River Aksu').add_to(m)
folium.GeoJson(basin_gdf.to_json(), name='Basin of Aksu').add_to(m)

for index, row in flood_probability_gdf.iterrows():
    folium.CircleMarker(
        location=[43.5, 106.0],  # Пример координат (замените на реальные данные)
        radius=10,
        popup=f'Probability of Flood: {row["probability"]:.2f}',
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("229.html")