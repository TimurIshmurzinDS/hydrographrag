import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть временные ряды данных для уровней воды рек Лепси Ривер и Шилик Ривер.
# Для примера создадим синтетические данные.

# Создание синтетических данных
np.random.seed(0)
dates = pd.date_range(start='2020-01-01', end='2023-12-31')
lepsy_river_level = 5 + np.sin(np.linspace(0, 6*np.pi, len(dates))) * 2 + np.random.normal(0, 0.5, len(dates))
shilik_river_level = 4 + np.cos(np.linspace(0, 6*np.pi, len(dates))) * 1.5 + np.random.normal(0, 0.3, len(dates))

data = pd.DataFrame({
    'Date': dates,
    'Lepsy_River_Level': lepsy_river_level,
    'Shilik_River_Level': shilik_river_level
})

# Преобразование столбца дат в индекс
data.set_index('Date', inplace=True)

# Визуализация временных рядов
plt.figure(figsize=(14, 7))
plt.plot(data['Lepsy_River_Level'], label='Уровень воды Лепси Ривер')
plt.plot(data['Shilik_River_Level'], label='Уровень воды Шилик Ривер')
plt.title('Временные ряды уровней воды рек Лепси и Шилик')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Декомпозиция временных рядов для выявления сезонных компонент
decomposition_lepsy = seasonal_decompose(data['Lepsy_River_Level'], model='additive', period=12)
decomposition_shilik = seasonal_decompose(data['Shilik_River_Level'], model='additive', period=12)

# Визуализация декомпозиции для Лепси Ривер
plt.figure(figsize=(14, 7))
plt.subplot(411)
plt.plot(data['Lepsy_River_Level'], label='Исходные данные')
plt.legend(loc='upper left')
plt.subplot(412)
plt.plot(decomposition_lepsy.trend, label='Тренд')
plt.legend(loc='upper left')
plt.subplot(413)
plt.plot(decomposition_lepsy.seasonal,label='Сезонная компонента')
plt.legend(loc='upper left')
plt.subplot(414)
plt.plot(decomposition_lepsy.resid, label='Остатки')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Визуализация декомпозиции для Шилик Ривер
plt.figure(figsize=(14, 7))
plt.subplot(411)
plt.plot(data['Shilik_River_Level'], label='Исходные данные')
plt.legend(loc='upper left')
plt.subplot(412)
plt.plot(decomposition_shilik.trend, label='Тренд')
plt.legend(loc='upper left')
plt.subplot(413)
plt.plot(decomposition_shilik.seasonal,label='Сезонная компонента')
plt.legend(loc='upper left')
plt.subplot(414)
plt.plot(decomposition_shilik.resid, label='Остатки')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Создание карты с использованием folium
m = folium.Map(location=[53.9023, 27.5619], zoom_start=8)  # Координаты Минска для примера

# Добавление маркеров для рек Лепси Ривер и Шилик Ривер
folium.Marker([54.0000, 27.3333], popup='Лепси Ривер').add_to(m)
folium.Marker([53.8961, 27.5598], popup='Шилик Ривер').add_to(m)

# Сохранение карты в файл
m.save("152.html")