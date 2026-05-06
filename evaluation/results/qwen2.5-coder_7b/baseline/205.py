import pandas as pd
import folium
from datetime import datetime

# Загрузка данных
data = {
    'date': ['2018-01-01', '2019-01-01', '2020-01-01', '2021-01-01'],
    'snowmelt_start': ['2018-03-15', '2019-03-10', '2020-03-20', '2021-03-18'],
    'water_level': [10, 12, 14, 16]
}

df = pd.DataFrame(data)

# Преобразование дат в формат datetime
df['date'] = pd.to_datetime(df['date'])
df['snowmelt_start'] = pd.to_datetime(df['snowmelt_start'])

# Создание столбца для длительности снеготаяния
df['duration'] = (df['snowmelt_start'] - df['date']).dt.days

# Анализ временных рядов
print(df)

# Визуализация данных на карте
m = folium.Map(location=[50.45, 30.52], zoom_start=12)

for index, row in df.iterrows():
    folium.Marker([50.45, 30.52],
                  popup=f"Дата: {row['date']}\nДлительность снеготаяния: {row['duration']} дней\nУровень воды: {row['water_level']} м",
                  icon=folium.Icon(color='blue')).add_to(m)

m.save("205.html")