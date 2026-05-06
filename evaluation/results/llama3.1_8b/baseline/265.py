import pandas as pd
from folium import Map, Marker

# Шаг 1: Сбор данных
data = {
    'координаты': [(55.7558, 37.6173), (55.7559, 37.6174)],
    'уровень загрязнения': [10, 20],
    'количество погибших животных': [100, 200]
}

df = pd.DataFrame(data)

# Шаг 2: Создание модели
def calculate_pollution_level(zagranenie):
    return zagranenie * 0.1

pollution_levels = df['уровень загрязнения'].apply(calculate_pollution_level)

# Шаг 3: Анализ данных
df['прогнозированное количество погибших животных'] = pollution_levels * 10

# Шаг 4: Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=12)

for index, row in df.iterrows():
    Marker(
        location=row['координаты'],
        popup=f'Уровень загрязнения: {row["уровень загрязнения"]}<br>Количество погибших животных: {row["количество погибших животных"]}',
        icon=folium.Icon(color='red')
    ).add_to(m)

m.save("265.html")