import pandas as pd
from folium import Map, Marker
from datetime import datetime

# Загрузка данных
bayankol_data = pd.read_csv('bayankol_flow.csv')
kishi_almaty_data = pd.read_csv('kishi_almaty_flow.csv')

# Подготовка данных для моделирования
bayankol_data['date'] = pd.to_datetime(bayankol_data['date'])
kishi_almaty_data['date'] = pd.to_datetime(kishi_almaty_data['date'])

bayankol_mean_volatility = bayankol_data.groupby('date')['bayankol_flow'].std().mean()
kishi_almaty_mean_volatility = kishi_almaty_data.groupby('date')['kishi_almaty_flow'].std().mean()

# Сравнение волатильности стока
if bayankol_mean_volatility > kishi_almaty_mean_volatility:
    print("Волатильность стока в реке Bayankol выше, чем в реке Kishi Almaty.")
else:
    print("Волатильность стока в реке Bayankol ниже или равна волатильности стока в реке Kishi Almaty.")

# Визуализация результатов на карте
m = Map(location=[43.0, 76.5], zoom_start=10)

if bayankol_mean_volatility > kishi_almaty_mean_volatility:
    Marker([43.2, 76.8], popup='Волатильность стока в реке Bayankol выше').add_to(m)
    Marker([42.1, 77.3], popup='Волатильность стока в реке Kishi Almaty ниже').add_to(m)

m.save("134.html")