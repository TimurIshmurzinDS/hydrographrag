import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import MarkerCluster

# Пример данных: уровень реки и потребление воды животноводческими хозяйствами
data = {
    'Level_River': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    'Water_Consumption': [100, 120, 140, 160, 180, 200, 220, 240, 260, 280]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Построение модели линейной регрессии
model = LinearRegression()
X = df[['Level_River']]
y = df['Water_Consumption']
model.fit(X, y)

# Прогнозирование потребления воды при снижении уровня реки
new_levels = np.linspace(1, 0, 50)
predicted_consumption = model.predict(new_levels.reshape(-1, 1))

# Визуализация результатов на карте
m = folium.Map(location=[43.2689, 76.9290], zoom_start=10)

# Добавление точек с данными о потреблении воды и уровне реки
for lat, lon, level, consumption in zip(df['Latitude'], df['Longitude'], df['Level_River'], df['Water_Consumption']):
    folium.Marker([lat, lon], popup=f"Уровень реки: {level}, Потребление воды: {consumption}").add_to(m)

# Добавление линии прогноза
folium.PolyLine(locations=list(zip(new_levels, predicted_consumption)), color='red', weight=2.5).add_to(m)

# Сохранение карты
m.save("187.html")