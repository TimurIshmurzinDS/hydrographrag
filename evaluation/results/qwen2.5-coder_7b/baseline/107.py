import folium
from shapely.geometry import Polygon, shape
from geopandas import GeoDataFrame

# Пример данных: площади земли для сельского хозяйства в квадратных метрах
areas = {
    'Tekeli River': 100000,
    'Temirlik River': 50000
}

# Пример данных: потребление воды на единицу площади земли для сельского хозяйства в литрах в день
water_consumption_per_unit_area = 200

# Расчет суммарного потребления воды
total_water_consumption = sum(areas.values()) * water_consumption_per_unit_area / 1000000  # Переводим в миллилитры

print(f"Суммарное потребление воды для нужд сельского хозяйства по рекам Tekeli River и Temirlik River: {total_water_consumption:.2f} миллионов литров в день")

# Визуализация на карте
m = folium.Map(location=[40.7128, 30.3659], zoom_start=6)

for river, area in areas.items():
    # Пример координат для демонстрации (замените на реальные данные)
    coords = [
        (40.7128, 30.3659),
        (40.7128, 30.3669),
        (40.7138, 30.3669),
        (40.7138, 30.3659)
    ]
    
    polygon = Polygon(coords)
    gdf = GeoDataFrame({'geometry': [polygon]})
    
    folium.GeoJson(gdf).add_to(m)

m.save("107.html")