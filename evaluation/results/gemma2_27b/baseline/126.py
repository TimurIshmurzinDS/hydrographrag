import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, FeatureGroup, GeoJson

# Загрузка данных (замените на ваши файлы)
shilik_data = pd.read_csv("shilik_river_flow.csv")
kishi_data = pd.read_csv("kishi_river_flow.csv")

# Обработка данных
shilik_data["Month"] = pd.to_datetime(shilik_data["Date"]).dt.month
kishi_data["Month"] = pd.to_datetime(kishi_data["Date"]).dt.month

monthly_avg_shilik = shilik_data.groupby("Month")["Flow"].mean()
monthly_avg_kishi = kishi_data.groupby("Month")["Flow"].mean()

# Визуализация

m = Map(location=[43, 78], zoom_start=6)

shilik_group = FeatureGroup(name="Shilik River").add_to(m)
plt.plot(monthly_avg_shilik.index, monthly_avg_shilik.values, marker='o')
plt.xlabel("Month")
plt.ylabel("Average Flow (m³/s)")
plt.title("Seasonal Variability of Shilik River Flow")

kishi_group = FeatureGroup(name="Kishi Almaty River").add_to(m)
plt.plot(monthly_avg_kishi.index, monthly_avg_kishi.values, marker='o')
plt.xlabel("Month")
plt.ylabel("Average Flow (m³/s)")
plt.title("Seasonal Variability of Kishi Almaty River Flow")

# Сохранение карты

m.save("126.html")