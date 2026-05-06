import geopandas as gpd
import folium
from shapely import wkt

def calculate_irrigation_need(water_level, target_level=5.0, coefficient=1.2, area=100):
    """
    Расчет потребности в поливе на основе уровня воды.
    :param water_level: Текущий уровень воды в реке (м)
    :param target_level: Целевой уровень воды (м)
    :param coefficient: Коэффициент водопотребности
    :param area: Площадь полива (га)
    :return: Объем необходимого полива (м3)
    """
    need = max(0, (target_level - water_level) * coefficient * area)
    return need

# 1. Загрузка данных бассейна
# Используем raw string для пути к файлу, согласно инструкции
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты Folium
# Центрирование карты по центроиду полигона бассейна
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Добавление слоя бассейна на карту
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 4. Обработка точек наблюдения (Поселок Баянколь)
# Поскольку WKT не предоставлены в контексте, создаем список объектов для демонстрации
observations = [
    {
        "name": "Bayankol village",
        "coords": [45.1234, 62.5678], # Примерные координаты
        "water_level": 3.2 # Текущее значение Water_level_Value
    }
]

# Расчет и добавление маркеров на карту
for obs in observations:
    irrigation_vol = calculate_irrigation_need(obs["water_level"])
    
    folium.Marker(
        location=obs["coords"],
        popup=f"Observation: {obs['name']}<br>Water Level: {obs['water_level']}m<br>Irrigation Need: {irrigation_vol:.2f} m3",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Сохранение итоговой карты
m.save("257.html")