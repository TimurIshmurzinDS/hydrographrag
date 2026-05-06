import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Каркара
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Каркара
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о потреблении воды (Water_consumption_Valuem³s) за последние 20 лет
water_data = [
    {"date": "2001-01-01", "value": 5.2},
    {"date": "2001-02-01", "value": 5.4},
    # ... данные за весь период с 2001 по 2020 год
    {"date": "2020-12-01", "value": 6.8}
]

# Преобразование данных в DataFrame для удобства анализа
import pandas as pd
water_df = pd.DataFrame(water_data)
water_df['date'] = pd.to_datetime(water_df['date'])

# Расчет среднего расхода воды за два периода
mean_consumption_last_decade = water_df[(water_df['date'] >= '2011-01-01') & (water_df['date'] <= '2020-12-31')]['value'].mean()
mean_consumption_previous_decade = water_df[(water_df['date'] >= '2001-01-01') & (water_df['date'] <= '2010-12-31')]['value'].mean()

# Расчет разницы в расходе воды
difference_in_consumption = mean_consumption_last_decade - mean_consumption_previous_decade

# Вывод результатов
print(f"Средний расход воды за последнее десятилетие: {mean_consumption_last_decade:.2f} м³/с")
print(f"Средний расход воды за предыдущее десятилетие: {mean_consumption_previous_decade:.2f} м³/с")
print(f"Разница в расходе воды: {difference_in_consumption:.2f} м³/с")

# Сохранение карты
m.save("54.html")