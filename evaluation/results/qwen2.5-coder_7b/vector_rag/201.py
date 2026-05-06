import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о количестве осадков и температуре (замените на реальные данные)
rainfall_data = [
    {'date': '2021-06-01', 'value': 50},
    {'date': '2021-06-02', 'value': 30},
    {'date': '2021-06-03', 'value': 40}
]

temperature_data = [
    {'date': '2021-06-01', 'value': 35},
    {'date': '2021-06-02', 'value': 38},
    {'date': '2021-06-03', 'value': 40}
]

# Пример данных о количестве осадков и температуре для прогнозирования (замените на реальные данные)
forecast_rainfall_data = [
    {'date': '2022-06-01', 'value': 55},
    {'date': '2022-06-02', 'value': 35},
    {'date': '2022-06-03', 'value': 45}
]

forecast_temperature_data = [
    {'date': '2022-06-01', 'value': 37},
    {'date': '2022-06-02', 'value': 40},
    {'date': '2022-06-03', 'value': 42}
]

# Определение пороговых значений засухи
rainfall_threshold = 30
temperature_threshold = 35

# Прогнозирование риска засухи
risk_of_drought = []
for i in range(len(forecast_rainfall_data)):
    if forecast_rainfall_data[i]['value'] < rainfall_threshold and forecast_temperature_data[i]['value'] > temperature_threshold:
        risk_of_drought.append({'date': forecast_rainfall_data[i]['date'], 'risk': 'High'})
    else:
        risk_of_drought.append({'date': forecast_rainfall_data[i]['date'], 'risk': 'Low'})

# Добавление информации о риске засухи на карту
for item in risk_of_drought:
    folium.Marker([centroid.y, centroid.x], popup=f"Date: {item['date']}, Risk of Drought: {item['risk']}").add_to(m)

# Сохранение карты
m.save("201.html")