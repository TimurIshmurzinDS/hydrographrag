import pandas as pd
import folium
from shapely.geometry import Point

# Шаг 1: Сбор данных о расходах воды в реках
# Предположим, что у нас есть данные о среднем месячном расходе воды (в кубических метрах в секунду)
data = {
    'River': ['Kurty River', 'Lepsy River'],
    'Average_Discharge_m3_s': [10.5, 7.2]  # Примерные данные
}

df = pd.DataFrame(data)

# Шаг 2: Анализ потребностей
# Предположим, что сельскохозяйственная потребность в воде составляет 5 кубических метров в секунду
agricultural_demand_m3_s = 5.0

# Шаг 3: Моделирование
df['Sufficient'] = df['Average_Discharge_m3_s'] >= agricultural_demand_m3_s

# Шаг 4: Визуализация на карте с использованием folium
# Координаты рек (примерные)
river_coordinates = {
    'Kurty River': [52.1607, 48.9275],
    'Lepsy River': [52.3155, 48.7522]
}

# Создание карты
m = folium.Map(location=[52.2370, 48.8566], zoom_start=10)

for index, row in df.iterrows():
    river_name = row['River']
    coordinates = river_coordinates[river_name]
    sufficient = row['Sufficient']
    
    # Определение цвета маркера
    color = 'green' if sufficient else 'red'
    
    # Добавление маркера на карту
    folium.Marker(
        location=coordinates,
        popup=f"{river_name}: {'Достаточно воды' if sufficient else 'Недостаточно воды'}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты в файл
m.save("120.html")

print(df)