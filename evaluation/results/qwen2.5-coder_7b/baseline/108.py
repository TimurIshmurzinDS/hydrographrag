import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровне стока рек (замените на реальные данные)
data = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'Kurty_River': [10, 12, 15, 18, 20],
    'Urzhar_River': [8, 9, 11, 13, 14]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Определение пороговых значений для экологического стресса
threshold_Kurty = df['Kurty_River'].quantile(0.95)
threshold_Urzhar = df['Urzhar_River'].quantile(0.95)

# Добавление столбца с меткой экологического стресса
df['Stress_Kurty'] = np.where(df['Kurty_River'] > threshold_Kurty, 'High', 'Low')
df['Stress_Urzhar'] = np.where(df['Urzhar_River'] > threshold_Urzhar, 'High', 'Low')

# Создание карты
m = folium.Map(location=[50.0, 36.0], zoom_start=10)

# Добавление точек на карте с меткой экологического стресса
for index, row in df.iterrows():
    folium.Marker(
        location=[50.0 + np.random.uniform(-0.1, 0.1), 36.0 + np.random.uniform(-0.1, 0.1)],
        popup=f"Date: {row['date']}\nKurty River: {row['Kurty_River']} (Stress: {row['Stress_Kurty']})\nUrzhar River: {row['Urzhar_River']} (Stress: {row['Stress_Urzhar']})"
    ).add_to(m)

# Сохранение карты
m.save("108.html")