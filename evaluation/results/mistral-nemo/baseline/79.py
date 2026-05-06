import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# 1. Подготовка данных
data = pd.read_csv('turgen_river_data.csv')
X = data[['flow_speed']]
y = data['water_level']

# 2. Обработка данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Анализ данных и построение модели
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Оценка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 5. Визуализация результатов
m = folium.Map(location=[50.7398, 69.2146], zoom_start=10) # Координаты реки Turgen River

for i in range(len(X_test)):
    folium.CircleMarker(
        location=(data.iloc[i]['latitude'], data.iloc[i]['longitude']),
        radius=np.sqrt(y_pred[i]) * 5,
        color='blue',
        fill=True
    ).add_to(m)

m.save("79.html")