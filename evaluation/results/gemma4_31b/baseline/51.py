import pandas as pd
import numpy as np
import folium
from datetime import datetime

# 1. Симуляция данных (так как реальный API гидропостов требует авторизации)
# Создаем синтетический набор данных за 3 года
np.random.seed(42)
dates = pd.date_range(start="2020-01-01", end="2022-12-31", freq='D')
# Симулируем сезонность: летом расход выше (паводки/таяние), зимой ниже
def generate_discharge(date):
    month = date.month
    if month in [6, 7, 8]:
        return np.random.normal(loc=15.0, scale=3.0) # Лето: средний 15 м3/с
    elif month in [12, 1, 2]:
        return np.random.normal(loc=5.0, scale=1.5)  # Зима: средний 5 м3/с
    else:
        return np.random.normal(loc=10.0, scale=2.0) # Остальное

discharge_values = [generate_discharge(d) for d in dates]
df = pd.DataFrame({'date': dates, 'discharge': discharge_values})

# 2. Предобработка и расчеты
df['month'] = df['date'].dt.month

# Определяем периоды
summer_months = [6, 7, 8]
winter_months = [12, 1, 2]

# Расчет средних значений
avg_summer = df[df['month'].isin(summer_months)]['discharge'].mean()
avg_winter = df[df['month'].isin(winter_months)]['discharge'].mean()
diff = avg_summer - avg_winter

print(f"Средний расход воды летом: {avg_summer:.2f} м3/с")
print(f"Средний расход воды зимой: {avg_winter:.2f} м3/с")
print(f"Разница: {diff:.2f} м3/с")

# 3. Геопространственная визуализация
# Координаты Kurty River (примерные координаты для визуализации в регионе Казахстана)
# В реальном проекте здесь используется GeoJSON или Shapefile
river_coords = [
    [43.512, 77.123], 
    [43.525, 77.150], 
    [43.540, 77.180], 
    [43.560, 77.210]
]

# Создание карты
m = folium.Map(location=[43.53, 77.16], zoom_start=12, tiles='OpenStreetMap')

# Отрисовка реки
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.8, 
    tooltip='Kurty River'
).add_to(m)

# Добавление информационного маркера с результатами анализа
info_text = (
    f"<b>Анализ расхода воды: Kurty River</b><br>"
    f"Средний расход (Лето): {avg_summer:.2f} м3/с<br>"
    f"Средний расход (Зима): {avg_winter:.2f} м3/с<br>"
    f"Разница: {diff:.2f} м3/с"
)

folium.Marker(
    location=[43.53, 77.16],
    popup=folium.Popup(info_text, max_width=300),
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("51.html")
print("Карта успешно сохранена в файл 51.html")