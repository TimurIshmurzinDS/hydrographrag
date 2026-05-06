import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (заменить на реальные данные)
water_consumption_data = [
    {"river": "Bayankol River", "year": 2018, "value_m3s": 50},
    {"river": "Bayankol River", "year": 2019, "value_m3s": 52},
    {"river": "Bayankol River", "year": 2020, "value_m3s": 48},
    {"river": "Bayankol River", "year": 2021, "value_m3s": 51},
    {"river": "Bayankol River", "year": 2022, "value_m3s": 53},
    {"river": "Tekes River", "year": 2018, "value_m3s": 70},
    {"river": "Tekes River", "year": 2019, "value_m3s": 72},
    {"river": "Tekes River", "year": 2020, "value_m3s": 68},
    {"river": "Tekes River", "year": 2021, "value_m3s": 71},
    {"river": "Tekes River", "year": 2022, "value_m3s": 74}
]

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(water_consumption_data)

# Вычисление среднего значения расхода воды за последние 5 лет для каждой реки
average_values = df.groupby('river')['value_m3s'].mean().reset_index()

# Предполагаемые текущие значения расхода воды (заменить на реальные данные)
current_values = {
    "Bayankol River": 60,
    "Tekes River": 80
}

# Вычисление разницы между текущим значением и средним значением для каждой реки
average_values['current_value'] = average_values['river'].map(current_values)
average_values['difference'] = average_values['current_value'] - average_values['value_m3s']

# Определение реки с наибольшим увеличением расхода воды
max_increase_river = average_values.loc[average_values['difference'].idxmax()]['river']
print(f"Река с наибольшим увеличением расхода воды: {max_increase_river}")

# Сохранение карты
m.save("125.html")