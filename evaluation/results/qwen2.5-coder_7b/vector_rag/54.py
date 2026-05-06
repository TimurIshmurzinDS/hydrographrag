import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о расходе воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2013-01', 'value': 100},
    {'date': '2013-02', 'value': 150},
    {'date': '2014-01', 'value': 120},
    {'date': '2014-02', 'value': 180},
    # Добавьте больше данных для обоих периодов
]

# Функция для агрегации данных по месяцам
def aggregate_data(data, period):
    aggregated = {}
    for item in data:
        year_month = item['date'][:7]
        if year_month not in aggregated:
            aggregated[year_month] = 0
        aggregated[year_month] += item['value']
    return {k: v / len([x for x in data if x['date'].startswith(k)]) for k, v in aggregated.items()}

# Агрегация данных для обоих периодов
last_decade_data = aggregate_data(water_consumption_data, '2013-')
previous_decade_data = aggregate_data(water_consumption_data, '2014-')

# Расчет разницы в расходе воды
difference = {}
for year_month in last_decade_data:
    if year_month in previous_decade_data:
        difference[year_month] = last_decade_data[year_month] - previous_decade_data[year_month]

# Визуализация результатов (пример использования matplotlib)
import matplotlib.pyplot as plt

months = list(difference.keys())
values = list(difference.values())

plt.figure(figsize=(10, 5))
plt.bar(months, values, color='blue')
plt.xlabel('Месяц')
plt.ylabel('Разница в расходе воды (м³)')
plt.title('Разница в расходе воды в реке Karkara River между последним и предыдущим десятилетиями')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Сохранение карты
m.save("54.html")