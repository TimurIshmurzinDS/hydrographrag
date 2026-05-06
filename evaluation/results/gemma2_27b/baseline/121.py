import pandas as pd
import matplotlib.pyplot as plt
import folium

# 1. Получение данных
data_bayankol = pd.read_csv("bayankol_river_flow.csv")
data_shilik = pd.read_csv("shilik_river_flow.csv")

# 2. Обработка данных
yearly_average_bayankol = data_bayankol.groupby("year").mean()["flow"]
yearly_average_shilik = data_shilik.groupby("year").mean()["flow"]

# 3. Сравнение
plt.figure(figsize=(10,6))
plt.bar(range(10), yearly_average_bayankol, label="Bayankol River")
plt.plot(range(10), yearly_average_shilik, marker="o", linestyle="-", label="Shilik River")
plt.xlabel("Year (relative)")
plt.ylabel("Average Flow (m³/s)")
plt.legend()
plt.title("Comparison of Average Water Flow in Bayankol and Shilik Rivers")

# 4. Картографирование
m = folium.Map(location=[50, 85], zoom_start=6)
folium.Marker(location=[51.23, 87.95], popup="Bayankol River").add_to(m)
folium.Marker(location=[49.83, 86.55], popup="Shilik River").add_to(m)

# Добавление графиков на карту (необходимо использовать folium.plugins.folium.GeoJson)

m.save("121.html")
plt.show()