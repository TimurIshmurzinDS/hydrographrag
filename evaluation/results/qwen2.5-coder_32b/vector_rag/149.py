import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных наблюдений (заменить на реальные данные)
observations = [
    {"river": "Лепса", "date_time": "2023-10-01 12:00:00", "water_level": 150.5},
    {"river": "Лепса", "date_time": "2023-10-01 12:10:00", "water_level": 151.0},
    {"river": "Киши Осек", "date_time": "2023-10-01 12:00:00", "water_level": 145.0},
    # Добавьте остальные наблюдения здесь
]

# Преобразование данных в DataFrame для анализа
import pandas as pd

df = pd.DataFrame(observations)
df['date_time'] = pd.to_datetime(df['date_time'])
df.sort_values(by=['river', 'date_time'], inplace=True)

# Проверка периодов отсутствия сигнала
missing_periods = []
for river in df['river'].unique():
    river_data = df[df['river'] == river]
    for i in range(1, len(river_data)):
        time_diff = (river_data.iloc[i]['date_time'] - river_data.iloc[i-1]['date_time']).total_seconds() / 60
        if time_diff > 15:  # Предполагаемый интервал между измерениями в минутах
            missing_periods.append({
                'river': river,
                'start_time': river_data.iloc[i-1]['date_time'],
                'end_time': river_data.iloc[i]['date_time']
            })

# Вывод периодов отсутствия сигнала
for period in missing_periods:
    print(f"Река: {period['river']}, Начало периода: {period['start_time']}, Конец периода: {period['end_time']}")

# Сохранение карты
m.save("149.html")