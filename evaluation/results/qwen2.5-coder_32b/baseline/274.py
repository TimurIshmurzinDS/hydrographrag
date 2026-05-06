import pandas as pd
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть CSV-файл с данными о добыче золота
# Структура файла: year, latitude, longitude, gold_mined (кг)

# Загрузка данных
data = pd.read_csv('gold_mining_data.csv')

# Преобразование столбца 'year' к целочисленному типу
data['year'] = data['year'].astype(int)

# Фильтрация данных для XIX и XX веков
xix_data = data[(data['year'] >= 1801) & (data['year'] <= 1900)]
xx_data = data[(data['year'] >= 1901) & (data['year'] <= 2000)]

# Агрегация данных по годам для каждого века
xix_annual_mining = xix_data.groupby('year')['gold_mined'].sum().reset_index()
xx_annual_mining = xx_data.groupby('year')['gold_mined'].sum().reset_index()

# Вывод динамики добычи золота по годам для XIX века
print("Динамика добычи золота в XIX веке:")
print(xix_annual_mining)

# Вывод динамики добычи золота по годам для XX века
print("\nДинамика добычи золота в XX веке:")
print(xx_annual_mining)

# Создание карты с использованием folium
m = folium.Map(location=[60, 100], zoom_start=4)

# Функция для добавления тепловой карты на основании данных о добыче золота
def add_heatmap(data, name):
    heatmap_data = data[['latitude', 'longitude', 'gold_mined']].values.tolist()
    HeatMap(heatmap_data, name=name).add_to(m)

# Добавление тепловых карт для XIX и XX веков
add_heatmap(xix_data, "XIX век")
add_heatmap(xx_data, "XX век")

# Добавление слоев управления на карте
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("274.html")