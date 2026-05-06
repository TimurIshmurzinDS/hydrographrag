import folium
import pandas as pd
import numpy as np

# Шаг 1: Сбор данных
# Для примера создадим искусственные данные о реке Аксу
data = {
    'latitude': [42.85, 42.86, 42.87, 42.88, 42.89],
    'longitude': [78.30, 78.31, 78.32, 78.33, 78.34],
    'elevation': [1500, 1600, 1700, 1800, 1900],  # Высота над уровнем моря
    'flow_rate': [20, 25, 30, 40, 50]  # Расход воды в кубических метрах в секунду
}

# Создание DataFrame из данных
df = pd.DataFrame(data)

# Шаг 2: Обработка данных
# В данном случае данные уже очищены и готовы к использованию

# Шаг 3: Моделирование
# Простая модель для демонстрации: увеличение расхода воды на 10% из-за весеннего павода
df['spring_flow_rate'] = df['flow_rate'] * 1.1

# Шаг 4: Визуализация
# Создание интерактивной карты с помощью folium
m = folium.Map(location=[42.86, 78.32], zoom_start=10)

# Добавление маркеров на карту для каждой точки данных
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Высота: {row['elevation']} м\nРасход воды (весна): {row['spring_flow_rate']} куб.м/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("237.html")