import pandas as pd
import folium

# Предполагается, что у нас есть CSV файлы с данными о уровнях воды для Лепсы и Текес.
# Формат данных: дата (YYYY-MM-DD), уровень воды (м)

# Шаг 1: Сбор данных
lepsy_data = pd.read_csv('lepsy_water_level.csv', parse_dates=['date'])
tekes_data = pd.read_csv('tekes_water_level.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
lepsy_data['year'] = lepsy_data['date'].dt.year
tekes_data['year'] = tekas_data['date'].dt.year

# Шаг 3: Анализ данных - находим год с самым высоким уровнем воды для Лепсы и Текес
max_lepsy_year = lepsy_data.groupby('year')['water_level'].idxmax()
max_tekes_year = tekas_data.groupby('year')['water_level'].idxmax()

lepsy_max_levels = lepsy_data.loc[max_lepsy_year, ['year', 'water_level']]
tekes_max_levels = tekas_data.loc[max_tekes_year, ['year', 'water_level']]

# Находим год с самым высоким уровнем воды среди всех лет для Лепсы и Текес
max_lepsy_overall = lepsy_max_levels.loc[lepsy_max_levels['water_level'].idxmax()]
max_tekes_overall = tekas_max_levels.loc[tekes_max_levels['water_level'].idxmax()]

# Вывод результатов
print(f"Год с самым высоким уровнем воды в реке Лепсы: {max_lepsy_overall['year']} ({max_lepsy_overall['water_level']:.2f} м)")
print(f"Год с самым высоким уровнем воды в реке Текес: {max_tekes_overall['year']} ({max_tekes_overall['water_level']:.2f} м)")

# Шаг 4: Визуализация
m = folium.Map(location=[43.0, 76.5], zoom_start=8)

# Координаты рек (примерные)
lepsy_coords = [42.9167, 76.5]
tekes_coords = [42.8333, 78.2]

folium.Marker(
    location=lepsy_coords,
    popup=f"Лепсы: {max_lepsy_overall['year']} ({max_lepsy_overall['water_level']:.2f} м)",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=tekes_coords,
    popup=f"Текес: {max_tekes_overall['year']} ({max_tekes_overall['water_level']:.2f} м)",
    icon=folium.Icon(color='green')
).add_to(m)

# Сохранение карты
m.save("132.html")