import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, FeatureGroup, GeoJson

# Загрузка данных о расходе воды
data_temirlik = pd.read_csv("temirlik_river_flow.csv", index_col="date")
data_turgen = pd.read_csv("turgen_river_flow.csv", index_col="date")

# Расчет среднемесячных значений расхода воды
monthly_mean_temirlik = data_temirlik.groupby(lambda x: x.month).mean()
monthly_mean_turgen = data_turirgen.groupby(lambda x: x.month).mean()

# Визуализация данных
plt.figure(figsize=(10, 6))
plt.plot(monthly_mean_temirlik["flow"], label="Temirlik River")
plt.plot(monthly_mean_turgen["flow"], label="Turgen River")
plt.xlabel("Month")
plt.ylabel("Flow (m³/s)")
plt.legend()

# Определение порогового значения для наводнения
threshold = 50 # Пример, нужно определить на основе данных

# Оценка угрозы наводнений
risk_temirlik = monthly_mean_temirlik["flow"] > threshold
risk_turgen = monthly_mean_turgen["flow"] > threshold

print("Risk of flooding:")
print(f"Temirlik River: {risk_temirlik}")
print(f"Turgen River: {risk_turgen}")

# Визуализация данных на карте (пример)
m = Map(location=[43.25, 76.9], zoom_start=8)

# Добавление данных о реках на карту
folium.GeoJson("rivers.geojson", name="Rivers").add_to(m)

# Сохранение карты
m.save("83.html")