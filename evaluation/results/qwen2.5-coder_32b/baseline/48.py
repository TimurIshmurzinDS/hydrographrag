import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, Marker, Popup, IFrame

# Шаг 1: Загрузка данных
data = pd.read_csv('karkara_river_discharge_2010-2020.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
data.sort_values(by='date', inplace=True)
data.dropna(subset=['discharge'], inplace=True)

# Шаг 3: Анализ данных
plt.figure(figsize=(14, 7))
plt.plot(data['date'], data['discharge'])
plt.title('Расход воды в реке Karkara River (2010-2020)')
plt.xlabel('Дата')
plt.ylabel('Расход воды, м³/с')
plt.grid(True)
plt.savefig('discharge_plot.png')  # Сохранение графика для использования на карте
plt.show()

# Шаг 4: Визуализация данных на карте с использованием folium
river_coordinates = (39.123, 47.456)  # Примерные координаты реки Karkara River

m = Map(location=river_coordinates, zoom_start=10)

# Добавление маркера на карту с графиком расхода воды
html = '<img src="discharge_plot.png" alt="Расход воды">'
iframe = IFrame(html, width=650, height=450)
popup = Popup(iframe, max_width=2650)

marker = Marker(location=river_coordinates, popup=popup)
marker.add_to(m)

# Сохранение карты в файл
m.save("48.html")