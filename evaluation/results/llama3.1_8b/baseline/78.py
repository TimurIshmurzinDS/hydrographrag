import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор и очистка данных
data = {
    'post': ['Post 1', 'Post 2', 'Post 3'],
    'water_flow': [100, 200, 300],
    'latitude': [45.1234, 46.5678, 47.9012],
    'longitude': [30.9876, 32.3456, 33.6789]
}

df = pd.DataFrame(data)

# Анализ данных
print(df.head())

# Создание модели
def predict_flood_probability(water_flow):
    if water_flow > 250:
        return 0.8
    elif water_flow > 150:
        return 0.5
    else:
        return 0.2

df['flood_probability'] = df['water_flow'].apply(predict_flood_probability)

# Визуализация результатов
m = Map(location=[46.5, 32.5], zoom_start=10)
for index, row in df.iterrows():
    Marker(location=[row['latitude'], row['longitude']], popup=f'Пост {row["post"]}: Вероятность наводнения - {row["flood_probability"] * 100}%').add_to(m)

HeatMap(data=df[['latitude', 'longitude']].values, radius=10).add_to(m)
m.save("78.html")