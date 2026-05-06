import pandas as pd
import folium

# Шаг 1: Сбор данных
lepys_data = pd.read_csv('lepys_water_levels.csv')
butak_data = pd.read_csv('butak_water_levels.csv')

# Шаг 2: Подготовка данных
lepys_data['date'] = pd.to_datetime(lepys_data['date'])
butak_data['date'] = pd.to_datetime(butak_data['date'])

# Шаг 3: Сравнение данных
lepys_mean_water_level = lepys_data['water_level'].mean()
butak_mean_water_level = butak_data['water_level'].mean()

print(f'Средний уровень воды в реке Лепсы: {lepys_mean_water_level}')
print(f'Средний уровень воды в реке Бутак: {butak_mean_water_level}')

# Шаг 4: Визуализация результатов
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

folium.Marker([lepys_data['latitude'].mean(), lepys_data['longitude'].mean()],
              popup='Река Лепсы').add_to(m)
folium.Marker([butak_data['latitude'].mean(), butak_data['longitude'].mean()],
              popup='Река Бутак').add_to(m)

m.save("138.html")