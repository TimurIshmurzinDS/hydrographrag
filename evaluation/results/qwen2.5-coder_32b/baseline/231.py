import pandas as pd
import numpy as np
import folium
from branca.colormap import LinearColormap

# Пример данных о водном уровне реки Коктал (датасет сгенерирован случайным образом)
np.random.seed(42)
dates = pd.date_range(start='2023-03-01', end='2023-05-31')
water_level = np.random.uniform(low=1.0, high=5.0, size=len(dates))
flow_speed = np.random.uniform(low=0.5, high=2.0, size=len(dates))

data = pd.DataFrame({
    'date': dates,
    'water_level': water_level,
    'flow_speed': flow_speed
})

# Определим периоды минимального риска половодья (например, когда уровень воды ниже 3 метров и скорость течения меньше 1.5 м/с)
data['risk'] = np.where((data['water_level'] < 3) & (data['flow_speed'] < 1.5), 'low', 'high')

# Создадим карту с отметками о риске
m = folium.Map(location=[42.8746, 74.5903], zoom_start=10)  # Координаты Коктала

colormap = LinearColormap(
    colors=['green', 'red'],
    vmin=0,
    vmax=1
)

# Добавим временные ряды на карту
for idx, row in data.iterrows():
    date_str = row['date'].strftime('%Y-%m-%d')
    risk_color = 'green' if row['risk'] == 'low' else 'red'
    folium.CircleMarker(
        location=[42.8746, 74.5903],  # Координаты Коктала
        radius=5,
        color=risk_color,
        fill=True,
        fill_color=risk_color,
        popup=f"Дата: {date_str}<br>Уровень воды: {row['water_level']} м<br>Скорость течения: {row['flow_speed']} м/с<br>Риск: {row['risk']}"
    ).add_to(m)

# Добавим легенду
colormap.add_to(m)

# Сохранение карты в файл
m.save("231.html")

# Вывод оптимальных дат для приготовления пасты
optimal_dates = data[data['risk'] == 'low']['date']
print("Оптимальные даты для приготовления пасты:")
for date in optimal_dates:
    print(date.strftime('%Y-%m-%d'))