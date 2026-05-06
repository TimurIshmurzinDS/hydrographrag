import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предположим, что данные о уровнях воды представлены в CSV файлах с колонками 'date' и 'water_level'
tekeli_data = pd.read_csv('tekeli_water_levels.csv', parse_dates=['date'])
lepsy_data = pd.read_csv('lepsy_water_levels.csv', parse_dates=['date'])

# Предварительная обработка данных
tekeli_data.dropna(inplace=True)
lepsy_data.dropna(inplace=True)

# Анализ стабильности уровня воды с использованием сезонного разложения
def analyze_stability(data, river_name):
    result = seasonal_decompose(data['water_level'], model='additive', period=365)
    
    plt.figure(figsize=(14, 8))
    plt.subplot(411)
    plt.plot(data['date'], data['water_level'])
    plt.title(f'Уровень воды в реке {river_name}')
    plt.subplot(412)
    plt.plot(result.trend)
    plt.title('Тренд')
    plt.subplot(413)
    plt.plot(result.seasonal)
    plt.title('Сезонность')
    plt.subplot(414)
    plt.plot(result.resid)
    plt.title('Остатки')
    plt.tight_layout()
    plt.show()

analyze_stability(tekeli_data, 'Tekeli River')
analyze_stability(lepsy_data, 'Lepsy River')

# Визуализация на карте с использованием folium
m = folium.Map(location=[41.3082, 69.2797], zoom_start=10)  # Координаты примерного центра региона

# Добавление маркеров для рек
folium.Marker([41.3500, 69.2500], popup='Tekeli River').add_to(m)
folium.Marker([41.2800, 69.3000], popup='Lepsy River').add_to(m)

# Добавление полигонов для областей риска (примерные координаты)
risk_area_tekeli = [[41.3500, 69.2500], [41.3600, 69.2600], [41.3700, 69.2500]]
folium.Polygon(locations=risk_area_tekeli, color='red', fill=True, fill_color='red').add_to(m)

risk_area_lepsy = [[41.2800, 69.3000], [41.2900, 69.3100], [41.3000, 69.3000]]
folium.Polygon(locations=risk_area_lepsy, color='red', fill=True, fill_color='red').add_to(m)

# Сохранение карты
m.save("116.html")