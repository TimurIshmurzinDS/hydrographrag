import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных
data = pd.read_csv('bayankol_river_data.csv')

# Предварительная обработка данных
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Выделение признаков и целевой переменной
features = data[['temperature', 'precipitation']]
target = data['flood']

# Разделение данных на обучение и тестирование
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовых данных
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"Date: {row['date']}\nTemperature: {row['temperature']}°C\nPrecipitation: {row['precipitation']}mm\nFlood: {'Yes' if row['flood'] > 0 else 'No'}",
                  icon=folium.Icon(color='red' if row['flood'] > 0 else 'green')).add_to(m)

m.save("18.html")