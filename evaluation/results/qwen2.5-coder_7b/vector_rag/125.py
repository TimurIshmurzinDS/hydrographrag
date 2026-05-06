import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и потреблении воды
bayankol_river = {
    "name": "Bayankol River",
    "consumption_values": [100, 120, 130, 140, 150]  # Примерные значения потребления воды за последние 5 лет
}

tekes_river = {
    "name": "Tekes River",
    "consumption_values": [80, 90, 100, 110, 120]  # Примерные значения потребления воды за последние 5 лет
}

# Вычисление среднего значения потребления воды для каждой реки
bayankol_avg_consumption = sum(bayankol_river["consumption_values"]) / len(bayankol_river["consumption_values"])
tekes_avg_consumption = sum(tekes_river["consumption_values"]) / len(tekes_river["consumption_values"])

# Определение текущего значения потребления воды
current_bayankol_consumption = bayankol_river["consumption_values"][-1]
current_tekes_consumption = tekes_river["consumption_values"][-1]

# Вычисление увеличения расхода воды по сравнению со средним значением за последние 5 лет
bayankol_increase = (current_bayankol_consumption - bayankol_avg_consumption) / bayankol_avg_consumption * 100
tekes_increase = (current_tekes_consumption - tekes_avg_consumption) / tekes_avg_consumption * 100

# Определение реки с наибольшим увеличением расхода воды
if bayankol_increase > tekes_increase:
    result_river = "Bayankol River"
else:
    result_river = "Tekes River"

print(f"Река {result_river} показала наибольшее увеличение расхода воды по сравнению со своим средним значением за последние 5 лет.")

# Создание карты
m = folium.Map(location=[43.0, 76.0], tiles='CartoDB positron')

# Добавление границы бассейна (примерные координаты)
basin_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[75.0, 42.0], [76.0, 42.0], [76.0, 43.0], [75.0, 43.0], [75.0, 42.0]]]
            },
            "properties": {}
        }
    ]
}

folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты
m.save("125.html")