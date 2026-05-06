import pandas as pd
from folium import Map, TileLayer, Marker, Polygon
from folium.plugins import HeatMap

# Загрузка данных о текущем уровне воды в реке Шарын
water_level_data = pd.read_csv('water_level.csv')

# Загрузка данных о состоянии прилегающих экосистем и биоразнообразии
ecosystem_data = pd.read_csv('ecosystem_data.csv')

# Создание географического слоя для реки Шарын
river_layer = TileLayer(tiles='OpenStreetMap', name='Река Шарын').add_to(Map(location=[48.5, 87.0], zoom_start=10))

# Создание слоев для каждого типа экосистем
forest_layer = TileLayer(tiles='Stamen Terrain', name='Леса').add_to(river_layer)
steppe_layer = TileLayer(tiles='Stamen Terrain', name='Степи').add_to(river_layer)
waterbody_layer = TileLayer(tiles='Stamen Watercolor', name='Водоемы').add_to(river_layer)

# Применение метода моделирования изменения уровня воды в реке Шарын
def model_water_level_change(current_water_level, forecast):
    return current_water_level + forecast

# Оценка влияния изменения уровня воды на каждый тип экосистем и биоразнообразие
def evaluate_ecosystem_impact(ecosystem_type, water_level_change):
    if ecosystem_type == 'леса':
        return water_level_change * 0.5
    elif ecosystem_type == 'степи':
        return water_level_change * 0.3
    else:
        return water_level_change * 0.2

# Представление результатов в виде карты
def plot_results(water_level_data, ecosystem_data):
    heat_map = HeatMap(z=[evaluate_ecosystem_impact(ecosystem_type, model_water_level_change(current_water_level, forecast)) for current_water_level, forecast, ecosystem_type in zip(water_level_data['current_water_level'], water_level_data['forecast'], ecosystem_data['ecosystem_type'])], radius=10)
    heat_map.add_to(river_layer)

# Выполнение моделирования и представления результатов
plot_results(water_level_data, ecosystem_data)
m.save("181.html")