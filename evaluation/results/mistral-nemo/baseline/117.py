import pandas as pd
import numpy as np
from scipy import stats
import folium

# 1. Сбор данных о стоке рек Уржар и Аксу за определенный период времени.
data_urzhar = pd.read_csv('urzhar_river_discharge.csv')
data_aksu = pd.read_csv('aksu_river_discharge.csv')

# 2. Анализ изменений стока в обеих реках для выявления трендов и аномалий.
def analyze_discharge(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    trend, _ = stats.linregress(range(len(data)), data['discharge'])
    anomalies = data[(data['discharge'] > np.mean(data['discharge']) + 2*np.std(data['discharge'])) | (data['discharge'] < np.mean(data['discharge']) - 2*np.std(data['discharge']))]
    return trend, anomalies

trend_urzhar, anomalies_urzhar = analyze_discharge(data_urzhar)
trend_aksu, anomalies_aksu = analyze_discharge(data_aksу)

# 3. Определение нормальных значений стока для каждой реки на основе исторических данных.
normal_values_urzhar = data_urzhar['discharge'].mean()
normal_values_aksu = data_aksu['discharge'].mean()

# 4. Вычисление отклонений текущих значений стока от нормальных значений для каждой реки.
current_discharge_urzhar = data_urzhar['discharge'].iloc[-1]
current_discharge_aksu = data_aksu['discharge'].iloc[-1]

deviation_urzhar = abs(current_discharge_urzhar - normal_values_urzhar)
deviation_aksu = abs(current_discharge_aksu - normal_values_aksu)

# 5. Оценка экологического дисбаланса путем сравнения этих отклонений с заданными пороговыми значениями.
threshold = 100 # Заданное пороговое значение в кубических метрах

if deviation_urzhar > threshold:
    print("Экологический дисбаланс обнаружен в реке Уржар.")
else:
    print("Нет экологического дисбаланса в реке Уржар.")

if deviation_aksu > threshold:
    print("Экологический дисбаланс обнаружен в реке Аксу.")
else:
    print("Нет экологического дисбаланса в реке Аксу.")

# Визуализация данных на карте с использованием библиотеки folium.
m = folium.Map(location=[43.25, 76.9], zoom_start=8)

folium.Marker([data_urzhar['latitude'].mean(), data_urzhar['longitude'].mean()], popup='Уржар').add_to(m)
folium.Marker([data_aksu['latitude'].mean(), data_aksу['longitude'].mean()], popup='Аксу').add_to(m)

m.save("117.html")