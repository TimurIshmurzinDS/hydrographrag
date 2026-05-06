import pandas as pd
import matplotlib.pyplot as plt
import folium
import numpy as np

# 1. Подготовка данных (Синтетические данные для реки Sarykan)
# Расход воды в м3/с
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    '2020': [12.5, 14.2, 25.8, 45.1, 38.4, 20.1, 12.3, 8.5, 7.2, 9.1, 11.0, 13.2],
    '2023': [10.1, 12.8, 22.1, 38.5, 30.2, 15.4, 9.8, 6.1, 5.5, 7.8, 10.2, 11.5]
}

df = pd.DataFrame(data)

# Расчет разницы
df['Difference'] = df['2023'] - df['2020']
df['Pct_Change'] = (df['Difference'] / df['2020']) * 100

print("Сравнительная таблица расхода воды:")
print(df)

# 2. Визуализация данных (График)
plt.figure(figsize=(12, 6))
x = np.arange(len(df['Month']))
width = 0.35

plt.bar(x - width/2, df['2020'], width, label='2020', color='skyblue')
plt.bar(x + width/2, df['2023'], width, label='2023', color='salmon')

plt.xlabel('Месяц')
plt.ylabel('Расход воды (м3/с)')
plt.title('Сравнение ежемесячного расхода воды в реке Sarykan (2020 vs 2023)')
plt.xticks(x, df['Month'])
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 3. Геопространственная визуализация (Folium)
# Координаты Sarykan River (примерные координаты для региона)
river_coords = [
    [48.123, 65.456], 
    [48.150, 65.500], 
    [48.200, 65.550], 
    [48.250, 65.600]
]
station_coord = [48.123, 65.456] # Точка замера

# Создание карты
m = folium.Map(location=station_coord, zoom_start=10, tiles='OpenStreetMap')

# Добавление линии реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Sarykan River").add_to(m)

# Добавление маркера гидропоста
folium.Marker(
    location=station_coord,
    popup=f"Гидропост Sarykan\nСредний расход 2020: {df['2020'].mean():.2f} м3/с\nСредний расход 2023: {df['2023'].mean():.2f} м3/с",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("58.html")

print("\nАнализ завершен. Карта сохранена в файл 58.html")