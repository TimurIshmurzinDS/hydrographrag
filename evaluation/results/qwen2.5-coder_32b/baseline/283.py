import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Загрузка данных временных рядов
# Предположим, что у нас есть два CSV файла с данными о времени и значении
data1 = pd.read_csv('time_series_1.csv', parse_dates=['datetime'], index_col='datetime')
data2 = pd.read_csv('time_series_2.csv', parse_dates=['datetime'], index_col='datetime')

# Предварительная обработка данных
print("Пропущенные значения в первом временном ряду:")
print(data1.isnull().sum())
print("Пропущенные значения во втором временном ряду:")
print(data2.isnull().sum())

# Удаление пропусков (если необходимо)
data1.dropna(inplace=True)
data2.dropna(inplace=True)

# Выравнивание временных рядов
common_index = data1.index.intersection(data2.index)
aligned_data1 = data1.loc[common_index]
aligned_data2 = data2.loc[common_index]

# Визуализация временных рядов
plt.figure(figsize=(14, 7))
sns.lineplot(data=aligned_data1, x=aligned_data1.index, y='value', label='Временной ряд 1')
sns.lineplot(data=aligned_data2, x=aligned_data2.index, y='value', label='Временной ряд 2')
plt.title('Сравнение двух временных рядов')
plt.xlabel('Дата и время')
plt.ylabel('Значение')
plt.legend()
plt.grid(True)
plt.show()

# Анализ и метрики
mean1 = aligned_data1['value'].mean()
mean2 = aligned_data2['value'].mean()
std1 = aligned_data1['value'].std()
std2 = aligned_data2['value'].std()
correlation, _ = pearsonr(aligned_data1['value'], aligned_data2['value'])

print(f"Среднее значение первого временного ряда: {mean1}")
print(f"Среднее значение второго временного ряда: {mean2}")
print(f"Стандартное отклонение первого временного ряда: {std1}")
print(f"Стандартное отклонение второго временного ряда: {std2}")
print(f"Коэффициент корреляции между временными рядами: {correlation}")

# Если требуется визуализация на карте, предположим, что у нас есть координаты
# Для примера создадим фиктивные данные с координатами
import folium

# Создание фиктивных данных для карты
data_map = pd.DataFrame({
    'latitude': [55.7558, 59.9343],  # Координаты Москвы и Санкт-Петербурга
    'longitude': [37.6173, 30.3351],
    'value1': [mean1, mean2]
})

# Создание карты с помощью folium
m = folium.Map(location=[55.7558, 37.6173], zoom_start=4)

for _, row in data_map.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Среднее значение: {row['value1']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("283.html")