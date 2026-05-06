import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data = {
    'latitude': [51.23, 51.24, 51.25, 51.26],
    'longitude': [76.45, 76.46, 76.47, 76.48],
    'pH': [7.0, 6.9, 7.1, 7.2],
    'dissolved_oxygen': [8.0, 7.5, 8.5, 9.0],
    'bacteria_count': [100, 200, 150, 300]
}

df = pd.DataFrame(data)

# Преобразование данных
X = df[['pH', 'dissolved_oxygen']]
y = df['bacteria_count']

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Прогнозирование уровня загрязнения
predictions = model.predict(X)

# Добавление прогнозов в DataFrame
df['predicted_bacteria_count'] = predictions

# Создание карты с использованием folium
m = folium.Map(location=[51.24, 76.46], zoom_start=13)

for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"pH: {row['pH']}, DO: {row['dissolved_oxygen']}, Bacteria Count: {int(row['bacteria_count'])}, Predicted Bacteria Count: {int(row['predicted_bacteria_count'])}",
        icon=folium.Icon(color='red' if row['predicted_bacteria_count'] > 250 else 'green')
    ).add_to(m)

# Сохранение карты
m.save("40.html")