import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Шаг 1: Подготовка данных
data = {
    'Поле': ['Поле 1', 'Поле 2', 'Поле 3'],
    'Широта': [42.1234, 42.4567, 42.7890],
    'Долгота': [71.2345, 71.5678, 71.8901]
}

df = pd.DataFrame(data)

# Шаг 2: Создание геометрии полей и бассейна
bassin = {
    'Широта': [42.1234, 42.4567, 42.7890],
    'Долгота': [71.2345, 71.5678, 71.8901]
}

# Шаг 3: Создание модели автоматического полива
def calculate_water_need(field):
    # Простая модель для демонстрации
    return field['Широта'] * field['Долгота']

water_needs = df.apply(calculate_water_need, axis=1)

# Шаг 4: Визуализация результатов
m = Map(location=[42.5, 71.5], zoom_start=10)
for index, row in df.iterrows():
    Marker([row['Широта'], row['Долгота']], popup=f'Поле {index+1}').add_to(m)

HeatMap(data=df[['Широта', 'Долгота']].values, radius=20).add_to(m)
m.save("266.html")