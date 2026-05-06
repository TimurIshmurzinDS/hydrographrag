import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, Marker

# Сбор и подготовка данных (предположим, что данные хранятся в файлах Koksu_data.csv и Emel_data.csv)
koksu_data = pd.read_csv('Koksudata.csv')
emel_data = pd.read_csv('Emeldata.csv')

# Объединение данных обеих рек
data = pd.concat([koksu_data, emel_data])

# Подготовка данных для анализа
data['date'] = pd.to_datetime(data['date'])
data['month'] = data['date'].dt.month

# Анализ сезонных закономерностей
koksu_max = data[data['river'] == 'Koksudata']['water_flow'].groupby(data['month']).mean()
emel_max = data[data['river'] == 'Emeldata']['water_flow'].groupby(data['month']).mean()

plt.figure(figsize=(10,6))
plt.plot(koksu_max.index, koksu_max.values, label='Koksudata')
plt.plot(emel_max.index, emel_max.values, label='Emeldata')
plt.xlabel('Месяц')
plt.ylabel('Средний расход воды (м³/с)')
plt.title('Сезонные закономерности расхода воды в реках Koksu и Emel')
plt.legend()
plt.show()

# Визуализация результатов на карте
m = Map(location=[45.0, 75.0], zoom_start=6)
Marker(location=[45.0, 75.0], popup='Река Koksu').add_to(m)
Marker(location=[40.0, 70.0], popup='Река Emel').add_to(m)

# Сохранение карты в файл
m.save("196.html")