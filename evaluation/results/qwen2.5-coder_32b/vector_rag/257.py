import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Баянколь
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Баянколь
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды в реке Баянколь (Water_level_Value)
# Предполагается, что данные доступны и могут быть использованы для расчетов
water_levels = [
    {'date': '2023-10-01', 'level': 150},
    {'date': '2023-10-02', 'level': 145},
    {'date': '2023-10-03', 'level': 160}
]

# Пример данных о поселке Баянколь (Bayankol village)
# Предполагается, что координаты в формате WKT доступны
observations = [
    {'name': 'Bayankol village', 'coordinates': wkt.loads('POINT(85.29 47.13)')}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Пример расчета потребности в поливе на основе уровня воды
# Предполагается, что нормативный уровень воды для полива - 150 единиц
irrigation_need = []
for level in water_levels:
    if level['level'] < 150:
        irrigation_need.append({'date': level['date'], 'need': True})
    else:
        irrigation_need.append({'date': level['date'], 'need': False})

# Вывод результатов расчета потребности в поливе
for need in irrigation_need:
    print(f"Дата: {need['date']}, Необходимость в поливе: {'Да' if need['need'] else 'Нет'}")

# Сохранение карты
m.save("257.html")