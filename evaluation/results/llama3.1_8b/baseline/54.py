import pandas as pd
import folium

# Подготовка данных (предположим, что данные хранятся в файле 'water_data.csv')
data = pd.read_csv('water_data.csv')

# Обработка и анализ данных
data['year'] = pd.to_datetime(data['date']).dt.year
data_last_decade = data[data['year'] >= 2010]
data_prev_decade = data[data['year'] < 2010]

# Рассчет разницы расхода воды
diff_water_usage = (data_last_decade['water_usage'].mean() - data_prev_decade['water_usage'].mean()) * 100

print(f'Разница в расходе воды между последним и предыдущим десятилетиями: {diff_water_usage:.2f}%')

# Визуализация результатов
m = folium.Map(location=[40.0, 50.0], zoom_start=6)
folium.Marker([40.0, 50.0], popup=f'Разница в расходе воды между последним и предыдущим десятилетиями: {diff_water_usage:.2f}%').add_to(m)

m.save('54.html')