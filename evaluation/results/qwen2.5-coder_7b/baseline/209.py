import geopandas as gpd
import folium
from shapely.geometry import Point

# Загрузка данных о бассейне Urzhar River (пример данных)
data = {
    'geometry': [Point(51.23, 76.45), Point(51.24, 76.46), Point(51.25, 76.47)],
    'elevation': [100, 150, 200]
}
gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')

# Определение регионов с высоким риском наводнений
threshold_elevation = 150  # Пороговая высота над уровнем моря для определения риска
gdf['risk'] = gdf['elevation'].apply(lambda x: 'High' if x > threshold_elevation else 'Low')

# Создание карты с использованием folium
m = folium.Map(location=[51.24, 76.46], zoom_start=10)

# Добавление слоя геометрии на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {
    'color': 'blue' if x['properties']['risk'] == 'Low' else 'red',
    'weight': 2,
    'fillOpacity': 0.5
}).add_to(m)

# Добавление маркеров с высотой над уровнем моря
for idx, row in gdf.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=f"Height: {row['elevation']} m").add_to(m)

# Сохранение карты в файл HTML
m.save("209.html")