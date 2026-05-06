import pandas as pd
import folium

# Шаг 1: Сбор данных
tekes_data = pd.read_csv('tekes_river_flood_data.csv')
bayankol_data = pd.read_csv('bayankol_river_flood_data.csv')

# Шаг 2: Подготовка данных
 tekes_data['River'] = 'Tekes River'
 bayankol_data['River'] = 'Bayankol River'

 combined_data = pd.concat([tekes_data, bayankol_data], ignore_index=True)

 # Шаг 3: Анализ данных
 average_tekes_flow = tekes_data['Flow'].mean()
 average_bayankol_flow = bayankol_data['Flow'].mean()

 print(f'Средний расход воды реки Tekes River во время паводков: {average_tekes_flow}')
 print(f'Средний расход воды реки Bayankol River во время паводков: {average_bayankol_flow}')

 # Шаг 4: Визуализация результатов
 m = folium.Map(location=[43.26, 71.85], zoom_start=8)  # Координаты и масштаб карты

 tekes_location = [43.26, 71.85]
 bayankol_location = [40.95, 67.58]

 folium.Marker(tekes_location, popup='Tekes River').add_to(m)
 folium.Marker(bayankol_location, popup='Bayankol River').add_to(m)

 # Шаг 5: Сохранение результатов
 m.save("25.html")