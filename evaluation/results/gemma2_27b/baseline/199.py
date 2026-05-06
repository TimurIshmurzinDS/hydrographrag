import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Загрузка данных осадков и стока рек
precip_data = pd.read_csv("precip_data.csv", index_col="Date")
urzh_flow = pd.read_csv("urzh_flow.csv", index_col="Date")
byzhy_flow = pd.read_csv("byzhy_flow.csv", index_col="Date")

# Расчет изменения осадков и стока за время
precip_change = precip_data["Precip"].pct_change()
urzh_flow_change = urzh_flow["Flow"].pct_change()
byzhy_flow_change = byzhy_flow["Flow"].pct_change()

# Расчет коэффициента корреляции
corr_urzh, _ = pearsonr(precip_change, urzh_flow_change)
corr_byzhy, _ = pearsonr(precip_change, byzhy_flow_change)

print("Коэффициент корреляции для реки Urzhar:", corr_urzh)
print("Коэффициент корреляции для реки Byzhy:", corr_byzhy)

# Визуализация на карте
m = folium.Map(location=[45, 60], zoom_start=8)

folium.Marker(location=[45.2, 61.5], popup="Urzhar River").add_to(m)
folium.Marker(location=[45.7, 62.5], popup="Byzhy River").add_to(m)

# Добавление графиков корреляции
fig_urzh = plt.figure()
plt.plot(precip_change, urzh_flow_change)
plt.xlabel("Изменение осадков")
plt.ylabel("Изменение стока Urzhar River")
folium.raster_layers.ImageOverlay(np.array(plt.imread(fig_urzh)), bounds=[45.1, 61.4, 45.3, 61.6]).add_to(m)

fig_byzhy = plt.figure()
plt.plot(precip_change, byzhy_flow_change)
plt.xlabel("Изменение осадков")
plt.ylabel("Изменение стока Byzhy River")
folium.raster_layers.ImageOverlay(np.array(plt.imread(fig_byzhy)), bounds=[45.6, 62.4, 45.8, 62.6]).add_to(m)

m.save("199.html")