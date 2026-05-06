import pandas as pd
import folium

# Загружаем данные о уровнях воды в реках и их географических координатах
data = pd.read_csv('river_data.csv')

# Определяем пороговый уровень воды (в этом примере мы используем 10 как пороговое значение)
threshold = 10

# Отфильтровываем реки с текущим уровнем воды выше порогового значения
high_water_rivers = data[data['water_level'] > threshold]

# Создаем карту и задаем центр по координатам первой реки из отфильтрованного списка
m = folium.Map(location=[high_water_rivers.iloc[0]['latitude'], high_water_rivers.iloc[0]['longitude']])

# Добавляем маркеры для рек с повышенным уровнем воды на карту
for index, row in high_water_rivers.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"{row['river_name']}: {row['water_level']} м").add_to(m)

# Сохраняем карту как HTML-файл
m.save("148.html")