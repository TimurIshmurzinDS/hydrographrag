import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 1. Генерация синтетических данных (имитация исторических данных)
# В реальном сценарии здесь будет загрузка CSV или API данных
np.random.seed(42)
dates = pd.date_range(start="2015-01-01", end="2023-12-31", freq='M')
n_months = len(dates)

# Имитируем сезонность (пик весной - апрель/май)
def seasonal_pattern(dates):
    return np.sin(2 * np.pi * (dates.month - 3) / 12) + 2

lepsy_levels = seasonal_pattern(dates) + np.random.normal(0, 0.5, n_months)
# Река Dos коррелирует с Lepsy, но с небольшим смещением и шумом
dos_levels = 0.7 * np.roll(lepsy_levels, 1) + 0.3 * np.random.normal(0, 1, n_months)
precipitation = np.random.gamma(2, 2, n_months)

df = pd.DataFrame({
    'date': dates,
    'lepsy_level': lepsy_levels,
    'dos_level': dos_levels,
    'precipitation': precipitation
})

# 2. Подготовка признаков для моделирования
# Создаем лаговые признаки (значения за прошлый месяц)
df['lepsy_lag1'] = df['lepsy_level'].shift(1)
df['precip_lag1'] = df['precipitation'].shift(1)
df['month'] = df['date'].dt.month
df = df.dropna()

X = df[['lepsy_lag1', 'precip_lag1', 'month']]
y = df['dos_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 3. Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Оценка вероятности паводка на следующий сезон (весна)
# Предположим, мы имеем данные за зиму и хотим предсказать апрель
current_lepsy = 2.5  # Текущий уровень Lepsy
current_precip = 12.0 # Текущие осадки
next_season_features = np.array([[current_lepsy, current_precip, 4]]) # Апрель

prediction = model.predict(next_season_features)[0]
std_dev = np.std(y_test - model.predict(X_test)) # Оценка ошибки модели

# Порог паводка (например, 90-й перцентиль исторических данных Dos)
flood_threshold = np.percentile(df['dos_level'], 90)

# Расчет вероятности через нормальное распределение (Z-score)
from scipy.stats import norm
prob_flood = 1 - norm.cdf(flood_threshold, loc=prediction, scale=std_dev)

print(f"Прогнозируемый уровень воды в реке Dos: {prediction:.2f}")
print(f"Порог паводка: {flood_threshold:.2f}")
print(f"Вероятность паводка в следующем сезоне: {prob_flood * 100:.2f}%")

# 5. Визуализация на карте
# Координаты (условные для региона, где могут быть такие реки)
coords_lepsy = [48.5, 75.0] 
coords_dos = [48.7, 75.3]

m = folium.Map(location=[48.6, 75.1], zoom_start=9, tiles='OpenStreetMap')

# Добавляем маркеры рек
folium.Marker(coords_lepsy, popup="Lepsy River (Source Data)", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(coords_dos, popup=f"Dos River (Prob. Flood: {prob_flood*100:.1f}%)", 
              icon=folium.Icon(color='red' if prob_flood > 0.5 else 'green')).add_to(m)

# Рисуем линию связи (гипотетический водосбор)
folium.PolyLine([coords_lepsy, coords_dos], color="blue", weight=2, opacity=0.8).add_to(m)

# Сохранение карты
m.save("128.html")
print("Карта сохранена в файл 128.html")