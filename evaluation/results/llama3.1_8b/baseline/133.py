import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Шаг 1: Скачать данные о недавших осадках и стоке реки Dos River.
dos_data = pd.read_csv('dos_river_data.csv')

# Шаг 2: Загрузить исторические данные стока реки Kurty River.
kurty_data = pd.read_csv('kurty_river_data.csv')

# Шаг 3: Создать модель, которая может сравнить влияние недавших осадков на сток реки Dos River относительно исторических данных реки Kurty River.
def compare_impact(dos_data, kurty_data):
    # Сравнить средний сток реки Dos River и Курты River
    avg_dos_flow = dos_data['flow'].mean()
    avg_kurty_flow = kurty_data['flow'].mean()

    # Рассчитать коэффициент сравнения
    comparison_factor = (avg_dos_flow / avg_kurty_flow) * 100

    return comparison_factor

comparison_factor = compare_impact(dos_data, kurty_data)

# Шаг 4: Визуализировать результаты на карте с помощью библиотеки `folium`.
m = Map(location=[55.7558, 37.6173], zoom_start=10)
Marker([55.7558, 37.6173], popup=f'Сравнение влияния недавших осадков: {comparison_factor}%').add_to(m)

# Сохранить карту в файл
m.save("133.html")