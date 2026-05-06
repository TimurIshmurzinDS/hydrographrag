import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
from datetime import datetime

# =============================================================================
# 1. Эмуляция получения данных (Data Acquisition)
# В реальном проекте здесь был бы запрос к API (например, ERA5 или GRDC)
# =============================================================================

def get_karkara_discharge_data(start_year=2010, end_year=2020):
    """
    Генерирует синтетические данные о расходе воды, имитирующие 
    сезонные колебания реки Karkara.
    """
    date_range = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq='D')
    n_days = len(date_range)
    
    # Создаем базовый сезонный цикл (синусоида) + случайный шум + тренд
    time = np.arange(n_days)
    seasonal_pattern = 50 * np.sin(2 * np.pi * time / 365.25) + 100
    noise = np.random.normal(0, 15, n_days)
    trend = np.linspace(0, -5, n_days) # Небольшое снижение расхода за 10 лет
    
    discharge = seasonal_pattern + noise + trend
    # Гарантируем, что расход не отрицательный
    discharge = np.maximum(discharge, 10)
    
    df = pd.DataFrame({'date': date_range, 'discharge_m3s': discharge})
    return df

# Получаем данные
data = get_karkara_discharge_data()

# =============================================================================
# 2. Анализ данных
# =============================================================================

# Расчет среднего расхода по годам
data['year'] = data['date'].dt.year
yearly_avg = data.groupby('year')['discharge_m3s'].mean()

print("Средний годовой расход воды в реке Karkara (м3/с):")
print(yearly_avg)

# Визуализация временного ряда (график)
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['discharge_m3s'], color='blue', linewidth=0.5)
plt.title("Исторический расход воды в реке Karkara (2010-2020)")
plt.xlabel("Год")
plt.ylabel("Расход (м3/с)")
plt.grid(True)
plt.savefig("discharge_plot.png")
plt.close()

# =============================================================================
# 3. Геопространственная визуализация (GIS)
# =============================================================================

# Координаты реки Karkara (примерные координаты для региона Эфиопии/Восточной Африки)
# Примечание: Точные координаты зависят от конкретного притока с таким названием
karkara_coords = [10.5, 39.5] 

# Создание карты
m = folium.Map(location=karkara_coords, zoom_start=8, tiles='OpenStreetMap')

# Добавление маркера гидрологической станции
folium.Marker(
    location=karkara_coords,
    popup=f"Станция мониторинга Karkara River<br>Период: 2010-2020<br>Средний расход: {data['discharge_m3s'].mean():.2f} м3/с",
    tooltip="Karkara River Discharge Station",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление круга влияния (бассейн реки)
folium.Circle(
    location=karkara_coords,
    radius=50000, # 50 км
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.2,
    popup="Приблизительная зона влияния станции"
).add_to(m)

# Сохранение карты строго в файл 48.html
m.save("48.html")

print("\nЗадача успешно выполнена.")
print("1. Данные сгенерированы и проанализированы.")
print("2. График сохранен как 'discharge_plot.png'.")
print("3. Интерактивная карта сохранена как '48.html'.")