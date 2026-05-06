import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два CSV файла: 'bayankol_water_level.csv' и 'gold_price.csv'
water_level_data = pd.read_csv('bayankol_water_level.csv', parse_dates=['date'])
gold_price_data = pd.read_csv('gold_price.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Выравнивание временных рядов и удаление пропусков
water_level_data.set_index('date', inplace=True)
gold_price_data.set_index('date', inplace=True)

merged_data = pd.merge(water_level_data, gold_price_data, on='date').dropna()

# Шаг 3: Анализ корреляции
plt.figure(figsize=(12, 6))
plt.plot(merged_data.index, merged_data['water_level'], label='Уровень воды')
plt.plot(merged_data.index, merged_data['gold_price'], label='Цена на золото', color='orange')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Уровень воды и цена на золото')
plt.legend()
plt.show()

# Шаг 4: Статистический анализ
correlation = merged_data['water_level'].corr(merged_data['gold_price'])
print(f'Коэффициент корреляции: {correlation}')

# Шаг 5: Моделирование
X = merged_data[['water_level']]
y = merged_data['gold_price']

model = LinearRegression()
model.fit(X, y)

# Прогнозирование цены на золото
merged_data['predicted_gold_price'] = model.predict(X)

# Шаг 6: Визуализация результатов
m = folium.Map(location=[45.039268, 71.587341], zoom_start=10)  # Координаты Байнахола

# Добавление маркеров с уровнями воды и прогнозируемыми ценами на золото
for idx, row in merged_data.iterrows():
    folium.Marker(
        location=[45.039268, 71.587341],  # Координаты Байнахола
        popup=f"Дата: {idx.strftime('%Y-%m-%d')}<br>Уровень воды: {row['water_level']}<br>Цена на золото: {row['gold_price']}<br>Прогнозируемая цена: {row['predicted_gold_price']:.2f}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

m.save("223.html")