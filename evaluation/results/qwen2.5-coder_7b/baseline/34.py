import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data = {
    'latitude': [50.1, 50.2, 50.3, 50.4],
    'longitude': [8.1, 8.2, 8.3, 8.4],
    'pollution_level': [10, 15, 20, 25]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование данных (например, нормализация)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['latitude', 'longitude']] = scaler.fit_transform(df[['latitude', 'longitude']])

# Разделение данных на признаки и целевую переменную
X = df[['latitude', 'longitude']]
y = df['pollution_level']

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Прогнозирование загрязнения воды на новых точках
new_data = pd.DataFrame({
    'latitude': [50.25],
    'longitude': [8.25]
})
new_data[['latitude', 'longitude']] = scaler.transform(new_data[['latitude', 'longitude']])
predicted_pollution = model.predict(new_data)

# Визуализация на карте
m = folium.Map(location=[np.mean(df['latitude']), np.mean(df['longitude'])], zoom_start=12)

for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Pollution Level: {row["pollution_level"]}', icon=folium.Icon(color='red')).add_to(m)

# Добавление прогнозируемого значения
predicted_marker = folium.Marker([new_data.iloc[0]['latitude'], new_data.iloc[0]['longitude']], 
                                  popup=f'Predicted Pollution Level: {predicted_pollution[0]:.2f}', 
                                  icon=folium.Icon(color='blue'))
predicted_marker.add_to(m)

# Сохранение карты
m.save("34.html")