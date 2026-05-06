import pandas as pd
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV-файл с данными о потреблении воды на фермерских хозяйствах.
# Файл содержит следующие столбцы: 'farm_id', 'latitude', 'longitude', 'water_consumption'

data = pd.read_csv('water_consumption_data.csv')

# Шаг 2: Обработка данных
# Проверка наличия пропущенных значений и удаление их, если необходимо
data.dropna(inplace=True)

# Шаг 3: Создание модели пространственного анализа
# В данном случае мы просто визуализируем точки на карте с цветовой градацией по уровню потребления воды

# Нормализация данных для цветовой градации
data['water_consumption_normalized'] = (data['water_consumption'] - data['water_consumption'].min()) / \
                                       (data['water_consumption'].max() - data['water_consumption'].min())

# Шаг 4: Визуализация результатов на карте
# Создание карты с центром в районе реки Аксу
m = folium.Map(location=[42.8746, 75.9306], zoom_start=10)  # Координаты примерно посередине реки Аксу

# Добавление маркеров на карту с цветовой градацией
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        color='blue',
        fill=True,
        fill_color=folium.colormap.linear.YlOrRd_09.scale(0, 1)(row['water_consumption_normalized']),
        fill_opacity=0.7,
        popup=f"Фермерское хозяйство {row['farm_id']}: Потребление воды - {row['water_consumption']} м³"
    ).add_to(m)

# Добавление легенды
folium.ColorLine(
    colors=['yellow', 'orange', 'red'],
    caption='Уровень потребления воды (м³)'
).add_to(m)

# Шаг 5: Сохранение карты в файл
m.save("41.html")