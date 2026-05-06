import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import folium

# 1. Симуляция исторических данных (так как реальный датасет не предоставлен)
# Создаем синтетические данные за последние 5 лет для реки Shilik
np.random.seed(42)
dates = pd.date_range(start="2019-01-01", end="2023-12-01", freq='MS')
# Генерация сезонного расхода воды (синусоида + шум)
# Пик обычно приходится на весну (апрель-май)
base_flow = 50 
seasonality = 30 * np.sin(2 * np.pi * (dates.month - 3) / 12)
noise = np.random.normal(0, 5, len(dates))
discharge_values = base_flow + seasonality + noise

df = pd.DataFrame({'date': dates, 'discharge': discharge_values})

# 2. Подготовка признаков (Feature Engineering)
def create_features(data):
    df_feat = data.copy()
    # Создаем лаги: расход за 1, 2 и 3 месяца до текущего
    df_feat['lag_1'] = df_feat['discharge'].shift(1)
    df_feat['lag_2'] = df_feat['discharge'].shift(2)
    df_feat['lag_3'] = df_feat['discharge'].shift(3)
    # Добавляем номер месяца для учета сезонности
    df_feat['month'] = df_feat['date'].dt.month
    return df_feat.dropna()

df_model = create_features(df)

# Разделение на X (признаки) и y (целевая переменная)
X = df_model[['lag_1', 'lag_2', 'lag_3', 'month']]
y = df_model['discharge']

# 3. Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Прогноз на следующий месяц (Январь 2024)
last_known_data = df['discharge'].tail(3).values[::-1] # Последние 3 значения
next_month = (dates[-1] + timedelta(days=31)).month

# Формируем вектор для предсказания: [lag_1, lag_2, lag_3, month]
X_next = np.array([[last_known_data[0], last_known_data[1], last_known_data[2], next_month]])
prediction = model.predict(X_next)[0]

print(f"Прогноз расхода воды на следующий месяц: {prediction:.2f} м3/с")

# 5. Геопространственная визуализация
# Координаты реки Shilik (примерные координаты в Казахстане)
shilik_coords = [48.5000, 82.5000] 

# Создание карты
m = folium.Map(location=shilik_coords, zoom_start=7, tiles='OpenStreetMap')

# Добавление маркера с результатом прогноза
popup_text = f"Река Shilik<br>Прогноз расхода на след. месяц: {prediction:.2f} м3/с"
folium.Marker(
    location=shilik_coords,
    popup=popup_text,
    tooltip="Прогноз расхода воды",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("47.html")
print("Карта сохранена в файл 47.html")