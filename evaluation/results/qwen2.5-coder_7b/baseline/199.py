import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
urzhar_river_data = pd.read_csv('urzhar_river_data.csv')
byzhy_river_data = pd.read_csv('byzhy_river_data.csv')

# Предварительный анализ и очистка данных
urzhar_river_data.dropna(inplace=True)
byzhy_river_data.dropna(inplace=True)

# Визуализация временных рядов осадков и стока для Urzhar River
plt.figure(figsize=(12, 6))
plt.plot(urzhar_river_data['date'], urzhar_river_data['precipitation'], label='Осадки')
plt.plot(urzhar_river_data['date'], urzhar_river_data['flow'], label='Сток')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Уrzhar River: Осадки и сток')
plt.legend()
plt.show()

# Визуализация временных рядов осадков и стока для Byzhy River
plt.figure(figsize=(12, 6))
plt.plot(byzhy_river_data['date'], byzhy_river_data['precipitation'], label='Осадки')
plt.plot(byzhy_river_data['date'], byzhy_river_data['flow'], label='Сток')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Byzhy River: Осадки и сток')
plt.legend()
plt.show()

# Корреляционный анализ для Urzhar River
correlation_urzhar = urzhar_river_data['precipitation'].corr(urzhar_river_data['flow'])
print(f'Корреляция между осадками и стоком в Urzhar River: {correlation_urzhar}')

# Корреляционный анализ для Byzhy River
correlation_byzhy = byzhy_river_data['precipitation'].corr(byzhy_river_data['flow'])
print(f'Корреляция между осадками и стоком в Byzhy River: {correlation_byzhy}')

# Моделирование (простой пример с использованием линейной регрессии)
from sklearn.linear_model import LinearRegression

# Для Urzhar River
X_urzhar = urzhar_river_data['precipitation'].values.reshape(-1, 1)
y_urzhar = urzhar_river_data['flow']
model_urzhar = LinearRegression()
model_urzhar.fit(X_urzhar, y_urzhar)

# Для Byzhy River
X_byzhy = byzhy_river_data['precipitation'].values.reshape(-1, 1)
y_byzhy = byzhy_river_data['flow']
model_byzhy = LinearRegression()
model_byzhy.fit(X_byzhy, y_byzhy)

# Визуализация моделей
plt.figure(figsize=(12, 6))
plt.scatter(urzhar_river_data['precipitation'], urzhar_river_data['flow'], label='Данные')
plt.plot(urzhar_river_data['precipitation'], model_urzhar.predict(X_urzhar), color='red', label='Модель')
plt.xlabel('Осадки')
plt.ylabel('Сток')
plt.title('Уrzhar River: Модель линейной регрессии')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.scatter(byzhy_river_data['precipitation'], byzhy_river_data['flow'], label='Данные')
plt.plot(byzhy_river_data['precipitation'], model_byzhy.predict(X_byzhy), color='red', label='Модель')
plt.xlabel('Осадки')
plt.ylabel('Сток')
plt.title('Byzhy River: Модель линейной регрессии')
plt.legend()
plt.show()

# Сохранение карты
m = folium.Map(location=[urzhar_river_data['latitude'].mean(), urzhar_river_data['longitude'].mean()], zoom_start=10)

# Добавление точек на карте для Urzhar River
for idx, row in urzhar_river_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Осадки: {row['precipitation']}, Сток: {row['flow']}").add_to(m)

# Добавление точек на карте для Byzhy River
for idx, row in byzhy_river_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Осадки: {row['precipitation']}, Сток: {row['flow']}").add_to(m)

m.save("199.html")