import pandas as pd
import matplotlib.pyplot as plt

# Предположим, что у нас есть CSV файл с данными о температуре на Марсе
# Структура файла: 'Date', 'Temperature'
data = {
    'Date': ['2012-08-06', '2013-08-05', '2014-08-04', '2015-08-03', '2016-08-02'],
    'Temperature': [-79.5, -78.2, -77.8, -78.5, -79.0]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Преобразуем столбец дат в формат datetime
df['Date'] = pd.to_datetime(df['Date'])

# Сортируем данные по дате
df.sort_values('Date', inplace=True)

# Построение графика изменения температуры на Марсе
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Temperature'], marker='o')
plt.title('Изменения температуры на поверхности Марса')
plt.xlabel('Дата')
plt.ylabel('Температура (°C)')
plt.grid(True)
plt.savefig("mars_temperature_changes.png")
plt.show()

# Поскольку данные не являются пространственными, мы не можем использовать folium для визуализации.
# Однако, если бы у нас были географические данные, мы могли бы создать карту следующим образом:
#
# import folium
# m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
# folium.Marker([45.5244, -122.6699]).add_to(m)
# m.save("284.html")

print("График изменения температуры сохранен как mars_temperature_changes.png")