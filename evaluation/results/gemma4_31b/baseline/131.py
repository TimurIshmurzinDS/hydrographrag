import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from datetime import datetime

# 1. Генерация синтетических данных (имитация исторических трендов)
# Создаем временной ряд за 5 лет (60 месяцев)
np.random.seed(42)
months = pd.date_range(start="2019-01-01", periods=60, freq='M')

def generate_river_flow(base, amplitude, noise_level):
    # Сезонный цикл: синусоида с пиком в июне (месяц 6)
    time = np.arange(60)
    seasonal = amplitude * np.sin(2 * np.pi * (time - 3) / 12)
    noise = np.random.normal(0, noise_level, 60)
    return base + seasonal + noise

# Расход воды для Sharyn River (как эталон/предиктор)
sharyn_flow = generate_river_flow(15, 8, 2)
# Расход воды для Kishi Almaty River (зависимая переменная с некоторым смещением и шумом)
# Предполагаем, что Kishi Almaty коррелирует с Sharyn, но имеет свои особенности
kishi_almaty_flow = 0.7 * sharyn_flow + np.random.normal(0, 1, 60)

df = pd.DataFrame({
    'Date': months,
    'Sharyn_Flow': sharyn_flow,
    'KishiAlmaty_Flow': kishi_almaty_flow
})

# 2. Моделирование (Линейная регрессия)
# Разделяем данные: используем первые 48 месяцев для обучения, последние 12 для теста/прогноза
train_df = df.iloc[:48]
test_df = df.iloc[48:]

X_train = train_df[['Sharyn_Flow']]
y_train = train_df['KishiAlmaty_Flow']
X_test = test_df[['Sharyn_Flow']]

model = LinearRegression()
model.fit(X_train, y_train)

# Прогноз среднемесячного расхода для Kishi Almaty на основе трендов Sharyn
predictions = model.predict(X_test)
test_df_pred = test_df.copy()
test_df_pred['Predicted_KishiAlmaty_Flow'] = predictions

print("Прогноз среднемесячного расхода воды для Kishi Almaty River:")
print(test_df_pred[['Date', 'Sharyn_Flow', 'Predicted_KishiAlmaty_Flow']].tail())

# 3. Геопространственная визуализация
# Координаты (приблизительные для демонстрации)
locations = {
    "Kishi Almaty River": [43.227, 76.920],
    "Sharyn River": [43.350, 79.500]
}

# Создание карты
m = folium.Map(location=[43.3, 78.2], zoom_start=6, tiles='OpenStreetMap')

# Добавление маркеров рек
for river, coords in locations.items():
    folium.Marker(
        location=coords,
        popup=f"{river}",
        icon=folium.Icon(color='blue' if 'Kishi' in river else 'green', icon='info-sign')
    ).add_to(m)

# Рисуем линию связи (символизирующую перенос тренда в модели)
line_coords = [locations["Kishi Almaty River"], locations["Sharyn River"]]
folium.PolyLine(line_coords, color="red", weight=2.5, opacity=0.8, dash_array='5, 10').add_to(m)

# Сохранение карты
m.save("131.html")

print("\nКарта сохранена в файл 131.html")