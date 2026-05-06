import pandas as pd
from folium import Map, Marker
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о наносах за последние 5 лет.
# Для простоты предположим, что данные хранятся в таблице Excel.
data = pd.read_excel('dos_river_data.xlsx')

# Шаг 2: Обработка и очистка данных от пропусков и аномалий.
# Удаление строк с пропусками
data.dropna(inplace=True)

# Удаление аномальных значений (например, значения больше среднего на 3 стандартных отклонения)
mean = data['load'].mean()
std = data['load'].std()
data = data[(data['load'] > mean - 3 * std) & (data['load'] < mean + 3 * std)]

# Шаг 3: Создание временного ряда для нагрузки наносов.
time_series = data.groupby('date')['load'].mean().reset_index()

# Шаг 4: Анализ временного ряда с помощью статистических методов.
print("Среднее значение:", time_series['load'].mean())
print("Медиана:", time_series['load'].median())
print("Дисперсия:", time_series['load'].std())

# Шаг 5: Визуализация результатов на карте с помощью библиотеки Folium.
m = Map(location=[40.0, -3.0], zoom_start=10)
for index, row in data.iterrows():
    Marker([row['lat'], row['lon']], popup=f"Нагрузка наносов: {row['load']}").add_to(m)

# Визуализация временного ряда
plt.figure(figsize=(10, 6))
plt.plot(time_series['date'], time_series['load'])
plt.title("Временной ряд нагрузки наносов")
plt.xlabel("Дата")
plt.ylabel("Нагрузка наносов")
plt.show()

# Сохранение карты в файл
m.save("56.html")