import pandas as pd
import folium

# Загрузить данные о уровнях паводка в реке Sharyn River и их исторических средних значениях
data = pd.read_csv('sharyn_river_flood_levels.csv')

# Вычислить разницу между максимальным зафиксированным уровнем паводка и его историческим средним значением для каждого измерения
data['flood_difference'] = data['max_flood_level'] - data['historical_mean']

# Создать карту с использованием библиотеки folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=8)

# Добавить маркеры на карту для каждого измерения, цвет которых зависит от разницы уровней паводка
for index, row in data.iterrows():
    if row['flood_difference'] > 0:
        color = 'red'
    else:
        color = 'green'
    folium.Marker([row['latitude'], row['longitude']], popup=f'Разница уровней паводка: {row["flood_difference"]}', icon=folium.Icon(color=color)).add_to(m)

# Сохранить карту в файл HTML
m.save("127.html")