import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Подготовка данных
animals_farms = gpd.read_file("animals_farms.shp")
river_levels = pd.read_csv("river_levels.csv")

# 2. Проанализировать влияние снижения уровня реки на доступность воды для животноводческих хозяйств
def analyze_water_access(farms, river_levels):
    # Рассчитать расстояние от каждого хозяйства до реки и использовать это для оценки влияния изменения уровня реки на доступность воды.
    pass

# 3. Оценить влияние на потребление воды
def evaluate_water_consumption(farms, river_levels):
    # Использовать данные о текущем потреблении воды в каждом животноводческом хозяйстве.
    # Рассчитать, как изменение доступности воды повлияет на потребление воды в каждом хозяйстве.
    # Суммировать изменения потребления воды во всех хозяйствах для получения общего влияния на потребление воды.
    pass

# 4. Визуализация результатов
def visualize_results(farms, river_levels):
    # Использовать библиотеку `folium` для визуализации местоположения животноводческих хозяйств, уровня реки и изменения доступности воды.
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

    # Добавить точки на карту для каждого животноводческого хозяйства
    for _, farm in farms.iterrows():
        folium.Marker([farm.geometry.y, farm.geometry.x]).add_to(m)

    # Сохранить финальную карту как "187.html"
    m.save("187.html")

# Выполнить моделирование и визуализацию
analyze_water_access(animals_farms, river_levels)
evaluate_water_consumption(animals_farms, river_levels)
visualize_results(animals_farms, river_levels)