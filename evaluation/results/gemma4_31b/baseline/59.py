import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium

# 1. Симуляция исторических данных (так как реальные данные реки Шилик требуют доступа к закрытым архивам)
# Создаем синтетический набор данных: год и максимальный расход воды (м3/с)
np.random.seed(42)
years = np.arange(1994, 2024)
# Генерируем данные с небольшим восходящим трендом и случайным шумом
max_discharge = 150 + 0.8 * (years - 1994) + np.random.normal(0, 15, len(years))

df = pd.DataFrame({'Year': years, 'Max_Discharge': max_discharge})

# 2. Построение прогностической модели
# Подготовка данных для LinearRegression
X = df[['Year']]
y = df['Max_Discharge']

model = LinearRegression()
model.fit(X, y)

# Прогноз на следующие 10 лет (2024-2033)
future_years = np.arange(2024, 2034).reshape(-1, 1)
predictions = model.predict(future_years)

# Создание DataFrame для прогноза
df_forecast = pd.DataFrame({'Year': future_years.flatten(), 'Predicted_Max_Discharge': predictions})

# 3. Визуализация результатов прогноза
plt.figure(figsize=(12, 6))
plt.scatter(df['Year'], df['Max_Discharge'], color='blue', label='Исторические максимумы')
plt.plot(df['Year'], model.predict(X), color='gray', linestyle='--', label='Линия тренда')
plt.plot(df_forecast['Year'], df_forecast['Predicted_Max_Discharge'], color='red', marker='o', label='Прогноз на 10 лет')
plt.title('Прогноз максимального расхода воды в реке Шилик')
plt.xlabel('Год')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True)
plt.show()

# 4. Геопространственная визуализация (GIS)
# Координаты реки Шилик (примерные координаты бассейна реки в Казахстане)
shilik_coords = [48.5, 81.5] 

# Создание карты
m = folium.Map(location=shilik_coords, zoom_start=7, tiles='OpenStreetMap')

# Добавление маркера реки
folium.Marker(
    location=shilik_coords,
    popup='Река Шилик: Область мониторинга расхода воды',
    tooltip='Shilik River',
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление текстового описания прогноза на карту
forecast_text = f"Прогноз макс. расхода на 2033 г.: {predictions[-1]:.2f} м3/с"
folium.Popup(forecast_text).add_to(m)

# Сохранение карты строго в файл 59.html
m.save("59.html")

print("Modeling complete. Forecast for the next decade generated.")
print(df_forecast)
print("Map saved as 59.html")