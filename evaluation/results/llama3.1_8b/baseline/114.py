import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Подготовка данных
data = {
    'River': ['Aksu River', 'Kurty River'],
    'Current Flow (m3/s)': [100, 50]
}
df = pd.DataFrame(data)

# Обработка данных
df['Irrigation Potential'] = df['Current Flow (m3/s)'] * 0.5  # Примерная формула для оценки ирригационного потенциала

# Моделирование
model_results = df.groupby('River')['Irrigation Potential'].mean().reset_index()

# Визуализация результатов
m = Map(location=[40, 70], zoom_start=6)
for index, row in model_results.iterrows():
    Marker([row['Current Flow (m3/s)'] * 0.1, row['River']], popup=f'Ирригационный потенциал: {row["Irrigation Potential"]}').add_to(m)

HeatMap(data=df[['Current Flow (m3/s)', 'River']].values, radius=10).add_to(m)
m.save("114.html")