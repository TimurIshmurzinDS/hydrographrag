import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import folium

# Пример данных (замените на реальные данные от датчиков)
data = {
    'temperature': [20, 25, 30, 18, 22, 24, 26, 27, 29, 31],
    'humidity': [40, 50, 60, 70, 80, 90, 85, 75, 65, 55],
    'soil_moisture': [30, 40, 50, 60, 70, 80, 90, 85, 75, 65],
    'suitable_for_cacti': [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]  # 1 - подходящие условия, 0 - не подходящие
}

df = pd.DataFrame(data)

# Разделение данных на признаки и целевую переменную
X = df[['temperature', 'humidity', 'soil_moisture']]
y = df['suitable_for_cacti']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели на тестовой выборке
accuracy = model.score(X_test, y_test)
print(f'Accuracy: {accuracy:.2f}')

# Прогнозирование для новых данных
new_data = pd.DataFrame({
    'temperature': [25],
    'humidity': [60],
    'soil_moisture': [70]
})

prediction = model.predict(new_data)
print(f'Prediction for new data: {prediction[0]}')

# Визуализация результатов на карте
m = folium.Map(location=[43.24, 76.91], zoom_start=12)

for index, row in df.iterrows():
    if row['suitable_for_cacti'] == 1:
        folium.Marker([row['latitude'], row['longitude']], popup='Подходящие условия для выращивания кактусов', icon=folium.Icon(color='green')).add_to(m)
    else:
        folium.Marker([row['latitude'], row['longitude']], popup='Не подходящие условия для выращивания кактусов', icon=folium.Icon(color='red')).add_to(m)

m.save("217.html")