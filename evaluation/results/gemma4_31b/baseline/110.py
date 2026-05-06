import pandas as pd
import numpy as np
import folium
from scipy import stats
import matplotlib.pyplot as plt

# 1. Симуляция данных (в реальном проекте здесь будет загрузка CSV или API)
# Создаем временной ряд за 10 лет
years = np.arange(2014, 2024)

# Расход воды (m3/s) - симулируем с некоторым разбросом
# Tekeli обычно крупнее Sarykan
data_tekeli_discharge = np.random.normal(loc=15, scale=3, size=10) 
data_sarykan_discharge = np.random.normal(loc=5, scale=1.5, size=10)

# Урожайность (т/га) - создаем зависимость от расхода воды + шум
# Урожайность = базовый уровень + коэффициент * расход + шум
yield_tekeli_zone = 2.0 + 0.15 * data_tekeli_discharge + np.random.normal(0, 0.2, 10)
yield_sarykan_zone = 1.5 + 0.20 * data_sarykan_discharge + np.random.normal(0, 0.2, 10)

df = pd.DataFrame({
    'Year': years,
    'Tekeli_Discharge': data_tekeli_discharge,
    'Sarykan_Discharge': data_sarykan_discharge,
    'Tekeli_Yield': yield_tekeli_zone,
    'Sarykan_Yield': yield_sarykan_zone
})

# 2. Статистический анализ (Корреляция)
corr_tekeli, p_tekeli = stats.pearsonr(df['Tekeli_Discharge'], df['Tekeli_Yield'])
corr_sarykan, p_sarykan = stats.pearsonr(df['Sarykan_Discharge'], df['Sarykan_Yield'])

print(f"Correlation Tekeli River: {corr_tekeli:.2f} (p-value: {p_tekeli:.4f})")
print(f"Correlation Sarykan River: {corr_sarykan:.2f} (p-value: {p_sarykan:.4f})")

# 3. Геопространственная визуализация
# Координаты (приблизительные для региона Казахстана/Центральной Азии)
coords_tekeli = [[44.1, 80.2], [44.3, 80.5], [44.5, 80.8]] # Линия реки
coords_sarykan = [[44.0, 81.0], [44.2, 81.3], [44.4, 81.6]] # Линия реки

# Создание карты
m = folium.Map(location=[44.2, 80.8], zoom_start=8, tiles='OpenStreetMap')

# Добавление рек на карту
folium.PolyLine(coords_tekeli, color="blue", weight=4, opacity=0.8, 
                tooltip="Tekeli River").add_to(m)
folium.PolyLine(coords_sarykan, color="cyan", weight=4, opacity=0.8, 
                tooltip="Sarykan River").add_to(m)

# Добавление маркеров гидропостов с информацией о корреляции
folium.CircleMarker(
    location=[44.3, 80.5],
    radius=10,
    popup=f"Tekeli River\nCorr with Yield: {corr_tekeli:.2f}",
    color="darkblue",
    fill=True,
    fill_color="darkblue"
).add_to(m)

folium.CircleMarker(
    location=[44.2, 81.3],
    radius=10,
    popup=f"Sarykan River\nCorr with Yield: {corr_sarykan:.2f}",
    color="darkcyan",
    fill=True,
    fill_color="darkcyan"
).add_to(m)

# Добавление текстового описания в виде всплывающего окна (опционально через HTML)
title_html = '''
    <h4 style="font-family: Arial;">Анализ влияния расхода воды на урожайность</h4>
    <p>Синие линии обозначают русла рек. Маркеры показывают точки анализа.</p>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Сохранение карты
m.save("110.html")

print("Modeling complete. Map saved as 110.html")