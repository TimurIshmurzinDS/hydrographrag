import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о течении реки Аксу и потреблении воды для сельского хозяйства
data = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'flow_rate': [50, 60, 70, 80],  # в м³/с
    'agriculture_water_consumption': [1000, 1200, 1300, 1400]  # в кубометрах
}

# Создание DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Вычисление объема воды, забираемого на нужды сельского хозяйства
df['water_taken_for_agriculture'] = df['agriculture_water_consumption']

# Визуализация данных на карте
m = folium.Map(location=[43.2167, 76.9083], zoom_start=10)

# Добавление точек с данными о потреблении воды для сельского хозяйства
for index, row in df.iterrows():
    folium.Marker(
        location=[43.2167, 76.9083],
        popup=f"Дата: {row['date']}\nПотребление воды для сельского хозяйства: {row['water_taken_for_agriculture']} кубометров",
        icon=folium.Icon(color='red', icon='drop')
    ).add_to(m)

# Сохранение карты
m.save("33.html")