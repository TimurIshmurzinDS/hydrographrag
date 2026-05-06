import pandas as pd
import numpy as np
import folium

# 1. Симуляция данных о расходе воды (так как реальные данные требуют доступа к API гидропостов)
# Создаем временной ряд за 20 лет (2004-2023)
np.random.seed(42)
years = np.arange(2004, 2024)
# Генерируем случайные значения расхода воды в м3/с с небольшим трендом на снижение
discharge_values = np.random.normal(loc=45, scale=10, size=20) - (np.arange(20) * 0.5)

df = pd.DataFrame({
    'Year': years,
    'Discharge': discharge_values
})

# 2. Расчет разницы между десятилетиями
# Предыдущее десятилетие: 2004-2013
prev_decade = df[df['Year'] <= 2013]['Discharge'].mean()
# Последнее десятилетие: 2014-2023
last_decade = df[df['Year'] > 2013]['Discharge'].mean()

diff = last_decade - prev_decade
percent_change = (diff / prev_decade) * 100

print(f"Средний расход (2004-2013): {prev_decade:.2f} м3/с")
print(f"Средний расход (2014-2023): {last_decade:.2f} м3/с")
print(f"Разница: {diff:.2f} м3/с ({percent_change:.2f}%)")

# 3. Геопространственная визуализация
# Координаты реки Karkara (примерные координаты для региона Эфиопии/Восточной Африки)
# В реальном проекте здесь используется GeoJSON файл русла реки
river_coords = [
    [10.123, 39.456], 
    [10.150, 39.500], 
    [10.200, 39.550], 
    [10.250, 39.600]
]
station_coord = [10.150, 39.500] # Точка замера

# Создание карты
m = folium.Map(location=station_coord, zoom_start=10, tiles='OpenStreetMap')

# Добавление линии реки
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.8, 
    tooltip='Karkara River'
).add_to(m)

# Добавление маркера с результатами анализа
popup_text = (
    f"<b>Анализ расхода воды: Karkara River</b><br>"
    f"Предыдущее десятилетие: {prev_decade:.2f} м3/с<br>"
    f"Последнее десятилетие: {last_decade:.2f} м3/с<br>"
    f"<b>Разница: {diff:.2f} м3/с ({percent_change:.2f}%)</b>"
)

folium.Marker(
    location=station_coord,
    popup=folium.Popup(popup_text, max_width=300),
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("54.html")
print("Карта успешно сохранена в файл 54.html")