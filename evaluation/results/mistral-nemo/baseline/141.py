import pandas as pd
import folium

# Загружаем данные о уровнях воды в реках из источника мониторинга
data = pd.read_csv('river_water_levels.csv')

# Отфильтровываем данные, чтобы получить только информацию об основных реках
main_rivers = ['River1', 'River2', 'River3']  # Замените на фактические названия основных рек
data_filtered = data[data['River'].isin(main_rivers)]

# Определяем пороговый уровень воды, который считается критическим
critical_level = 50  # Замените на фактический пороговый уровень воды

# Сравниваем текущие уровни воды с пороговым значением для каждой реки
data_filtered['Critical'] = data_filtered['WaterLevel'] > critical_level

# Визуализируем результаты на карте, используя библиотеку `folium`
m = folium.Map(location=[51.5074, -0.1278], zoom_start=4)  # Замените на фактические координаты центра карты

for index, row in data_filtered.iterrows():
    if row['Critical']:
        color = 'red'
    else:
        color = 'green'

    folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                        radius=5,
                        color=color).add_to(m)

# Сохраняем карту в файл HTML
m.save("141.html")