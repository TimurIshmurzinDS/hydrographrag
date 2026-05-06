import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных
data = pd.read_csv('karatal_river_data.csv')

# Предварительный анализ данных
print(data.head())
print(data.describe())

# Обработка данных
# Удаляем строки с пропущенными значениями
data.dropna(inplace=True)

# Разделение данных на признаки и целевую переменную
X = data[['temperature', 'flow_rate', 'pH']]
y = data['water_quality']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Water Quality: {row['water_quality']}",
        icon=folium.Icon(color='blue' if row['water_quality'] > 5 else 'red')
    ).add_to(m)

m.save("222.html")