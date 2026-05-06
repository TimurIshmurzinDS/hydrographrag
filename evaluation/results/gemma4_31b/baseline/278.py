import pandas as pd
import numpy as np
import folium
from sklearn.linear_model import LinearRegression
from scipy.spatial.distance import geodesic

# 1. Симуляция данных
# Города: Название, Широта, Долгота, Население, Индекс привлекательности (0-1)
cities_data = {
    'city': ['Moscow', 'St. Petersburg', 'Novosibirsk', 'Ekaterinburg', 'Krasnodar'],
    'lat': [55.7558, 59.9343, 55.0083, 56.8389, 45.0355],
    'lon': [37.6173, 30.3155, 82.9346, 60.6057, 38.9837],
    'pop': [12600000, 5400000, 1600000, 1500000, 1100000],
    'attractiveness': [0.9, 0.8, 0.5, 0.6, 0.7]
}
df_cities = pd.DataFrame(cities_data)

# Исторические данные о миграции (потоки за последние 3 года)
# Формат: Source, Target, Year, Volume
migration_history = [
    ['Novosibirsk', 'Moscow', 2021, 5000], ['Novosibirsk', 'Moscow', 2022, 5500], ['Novosibirsk', 'Moscow', 2023, 6200],
    ['Ekaterinburg', 'Moscow', 2021, 4000], ['Ekaterinburg', 'Moscow', 2022, 4300], ['Ekaterinburg', 'Moscow', 2023, 4800],
    ['Novosibirsk', 'St. Petersburg', 2021, 2000], ['Novosibirsk', 'St. Petersburg', 2022, 2100], ['Novosibirsk', 'St. Petersburg', 2023, 2300],
    ['Krasnodar', 'Moscow', 2021, 3000], ['Krasnodar', 'Moscow', 2022, 3100], ['Krasnodar', 'Moscow', 2023, 3000],
    ['Ekaterinburg', 'St. Petersburg', 2021, 1500], ['Ekaterinburg', 'St. Petersburg', 2022, 1600], ['Ekaterinburg', 'St. Petersburg', 2023, 1800],
]
df_hist = pd.DataFrame(migration_history, columns=['source', 'target', 'year', 'volume'])

# 2. Функция расчета расстояния
def get_distance(city1, city2):
    coords1 = (city1['lat'], city1['lon'])
    coords2 = (city2['lat'], city2['lon'])
    return geodesic(coords1, coords2).km

# 3. Моделирование и предсказание
predictions = []

# Перебираем все возможные пары городов
for i, src in df_cities.iterrows():
    for j, dst in df_cities.iterrows():
        if i.name == j.name: continue
        
        # А. Анализ тренда (Linear Regression)
        hist_pair = df_hist[(df_hist['source'] == src['city']) & (df_hist['target'] == dst['city'])]
        
        if not hist_pair.empty:
            X = hist_pair[['year']].values
            y = hist_pair['volume'].values
            model = LinearRegression().fit(X, y)
            trend_pred = model.predict([[2024]])[0]
        else:
            # Если данных нет, используем базовую гравитационную модель
            trend_pred = 0
            
        # Б. Гравитационный потенциал
        dist = get_distance(src, dst)
        # Формула: (Pop_src * Pop_dst * Attract_dst) / Dist^2
        gravity_pot = (src['pop'] * dst['pop'] * dst['attractiveness']) / (dist**2)
        
        # В. Итоговый прогноз (взвешенная сумма тренда и потенциала)
        # Для упрощения: если есть тренд, он доминирует, если нет - берем долю от потенциала
        if trend_pred > 0:
            final_pred = (trend_pred * 0.7) + (gravity_pot * 0.3)
        else:
            final_pred = gravity_pot * 0.01 # Коэффициент масштабирования для новых путей
            
        predictions.append({
            'source': src['city'], 'target': dst['city'], 
            'src_lat': src['lat'], 'src_lon': src['lon'],
            'dst_lat': dst['lat'], 'dst_lon': dst['lon'],
            'volume': final_pred
        })

df_pred = pd.DataFrame(predictions)

# 4. Визуализация с помощью Folium
m = folium.Map(location=[55, 60], zoom_start=3, tiles='CartoDB dark_matter')

# Добавляем маркеры городов
for _, row in df_cities.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color='cyan',
        fill=True,
        popup=row['city']
    ).add_to(m)

# Добавляем линии миграционных потоков
for _, row in df_pred.iterrows():
    if row['volume'] > 100: # Фильтр для отображения только значимых потоков
        # Толщина линии зависит от объема
        weight = max(1, row['volume'] / 1000)
        
        folium.PolyLine(
            locations=[[row['src_lat'], row['src_lon']], [row['dst_lat'], row['dst_lon']]],
            color='yellow',
            weight=weight,
            opacity=0.6,
            tooltip=f"From {row['source']} to {row['target']}: {int(row['volume'])} people"
        ).add_to(m)

# Сохранение карты
m.save("278.html")
print("Modeling complete. Map saved as 278.html")