import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# 1. Генерация синтетических данных (имитация исторических данных)
# В реальном сценарии здесь будет загрузка из CSV или API
np.random.seed(42)
dates = pd.date_range(start="2015-01-01", end="2024-12-31", freq='M')
n_months = len(dates)

# Река Dos (Предиктор): сезонные колебания + тренд + шум
dos_levels = 2.0 + 1.5 * np.sin(np.linspace(0, 2 * np.pi * 10, n_months)) + np.random.normal(0, 0.2, n_months)
# Река Lepsy (Цель): коррелирует с Dos, но с небольшим сдвигом и своим масштабом
lepsy_levels = 1.2 * dos_levels + 0.5 + np.random.normal(0, 0.1, n_months)

df = pd.DataFrame({'Date': dates, 'Dos_Level': dos_levels, 'Lepsy_Level': lepsy_levels})
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# 2. Подготовка данных для моделирования
X = df[['Dos_Level', 'Month', 'Year']]
y = df['Lepsy_Level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Обучение модели Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверка точности
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Mean Absolute Error: {mae:.4f}")

# 4. Прогноз на 2025 год
# Создаем данные для Dos на 2025 год (на основе среднего сезонного цикла)
dates_2025 = pd.date_range(start="2025-01-01", end="2025-12-31", freq='M')
dos_2025 = 2.0 + 1.5 * np.sin(np.linspace(2 * np.pi * 10, 2 * np.pi * 11, 12)) + np.random.normal(0, 0.2, 12)

X_2025 = pd.DataFrame({
    'Dos_Level': dos_2025,
    'Month': dates_2025.month,
    'Year': [2025] * 12
})

lepsy_2025_pred = model.predict(X_2025)

# Сохранение результатов прогноза
forecast_df = pd.DataFrame({'Date': dates_2025, 'Predicted_Lepsy_Level': lepsy_2025_pred})
print("\nForecast for Lepsy River 2025:")
print(forecast_df)

# 5. Геопространственная визуализация
# Координаты (примерные для демонстрации)
coords = {
    'Dos River': [48.5, 70.2],
    'Lepsy River': [48.7, 70.5]
}

m = folium.Map(location=[48.6, 70.3], zoom_start=9, tiles='OpenStreetMap')

# Добавление маркеров рек
for river, pos in coords.items():
    folium.Marker(
        location=pos,
        popup=f"{river} Monitoring Station",
        icon=folium.Icon(color='blue' if 'Dos' in river else 'green', icon='info-sign')
    ).add_to(m)

# Добавление линии, имитирующей связь между ними
folium.PolyLine(
    locations=[coords['Dos River'], coords['Lepsy River']],
    color='blue',
    weight=2,
    opacity=0.8,
    tooltip="Hydrological Correlation Path"
).add_to(m)

# Сохранение карты
m.save("124.html")
print("\nMap has been saved as 124.html")

# Визуализация прогноза (график)
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Lepsy_Level'], label='Historical Lepsy', color='blue')
plt.plot(forecast_df['Date'], forecast_df['Predicted_Lepsy_Level'], label='Predicted 2025', color='red', linestyle='--')
plt.title("Lepsy River Water Level Prediction")
plt.xlabel("Year")
plt.ylabel("Water Level (m)")
plt.legend()
plt.grid(True)
plt.show()