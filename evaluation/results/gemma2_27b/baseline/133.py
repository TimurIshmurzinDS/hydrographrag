import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузка данных осадков и стока
dos_precip = pd.read_csv("dos_precip.csv", index_col="Date")
kurty_flow = pd.read_csv("kurty_flow.csv", index_col="Date")

# Расчет среднего еженедельного стока для Dos River
weekly_mean_dos = dos_precip.resample("W").mean()

# Определение коэффициента корреляции между осадками и стоком для Kurty River
model = LinearRegression()
X = kurty_flow.values.reshape(-1, 1)
y = kurty_flow.index.values.reshape(-1, 1)
model.fit(X, y)

correlation = model.score(X, y)

# Визуализация результатов на карте
m = folium.Map(location=[dos_precip.index[0], dos_precip.values[0]], zoom_start=8)

folium.Marker(location=[dos_precip.index[0], dos_precip.values[0]], popup="Dos River").add_to(m)
folium.Marker(location=[kurty_flow.index[0], kurty_flow.values[0]], popup="Kurty River").add_to(m)

# Сохранение карты
m.save("133.html")