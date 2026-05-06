import pandas as pd
import folium
from datetime import timedelta

# Шаг 1: Сбор данных о уровнях воды в реках на протяжении времени.
data_bayankol = pd.read_csv('bayankol_water_levels.csv', parse_dates=['date'])
data_sarykan = pd.read_csv('sarykan_water_levels.csv', parse_dates=['date'])

# Шаг 2: Анализ данных для определения пиков уровней воды (паводков).
def find_flood_peaks(data):
    data['diff'] = data['water_level'].diff()
    peaks = data[data['diff'] > 0]['date']
    return peaks

bayankol_peaks = find_flood_peaks(data_bayankol)
sarykan_peaks = find_flood_peaks(data_sarykan)

# Шаг 3: Определение периодов времени между этими пиками для выявления наиболее опасных периодов паводка.
def find_dangerous_periods(peaks):
    periods = []
    for i in range(len(peaks) - 1):
        period_start = peaks[i]
        period_end = peaks[i + 1] - timedelta(days=7)
        periods.append((period_start, period_end))
    return periods

bayankol_dangerous_periods = find_dangerous_periods(bayankol_peaks)
sarykan_dangerous_periods = find_dangerous_periods(sarykan_peaks)

# Визуализация на карте с использованием библиотеки folium.
m = folium.Map(location=[43.25, 76.9], zoom_start=8) # Координаты и масштаб могут быть изменены в зависимости от местоположения рек.

for period in bayankol_dangerous_periods:
    folium.PolyLine(locations=[(period[0].latitude, period[0].longitude), (period[1].latitude, period[1].longitude)], color='red', weight=2.5).add_to(m)

for period in sarykan_dangerous_periods:
    folium.PolyLine(locations=[(period[0].latitude, period[0].longitude), (period[1].latitude, period[1].longitude)], color='blue', weight=2.5).add_to(m)

m.save("158.html")