import folium
import pandas as pd

# Шаг 1: Сбор данных о расходе воды в двух реках за последние 5 лет.
kurty_data = pd.read_csv('kurty_river_water_levels.csv')
tekes_data = pd.read_csv('tekes_river_water_levels.csv')

# Шаг 2: Очистка и предобработка данных для удаления любых некорректных или отсутствующих значений.
kurty_data.dropna(inplace=True)
tekes_data.dropna(inplace=True)

# Шаг 3: Агрегация данных по годам, чтобы получить средний расход воды для каждого года.
kurty_agg = kurty_data.groupby('year')['water_level'].mean()
tekes_agg = tekes_data.groupby('year')['water_level'].mean()

# Шаг 4: Создание двух списков содержащих средние значения расхода воды за каждый год.
kurty_list = [x for x in kurty_agg]
tekes_list = [x for x in tekes_agg]

# Шаг 5: Визуализация данных с помощью библиотеки `folium`.
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

folium.PolyLine(
    locations=[(43.1, 77), (43.3, 77)],
    weight=5,
    color='blue',
    opacity=0.8
).add_to(m)

folium.PolyLine(
    locations=[(42.9, 76.8), (43.1, 76.8)],
    weight=5,
    color='red',
    opacity=0.8
).add_to(m)

# Сохранение карты в файл HTML.
m.save("129.html")