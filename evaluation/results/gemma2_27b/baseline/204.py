import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных из CSV файлов
data_byzhy = pd.read_csv("byzhy_flow.csv", index_col="date")
data_urzhar = pd.read_csv("urzhar_flow.csv", index_col="date")

# Расчет статистических показателей
mean_byzhy = data_byzhy["flow"].mean()
std_byzhy = data_byzhy["flow"].std()
cv_byzhy = std_byzhy / mean_byzhy * 100

mean_urzhar = data_urzhar["flow"].mean()
std_urzhar = data_urzhar["flow"].std()
cv_urzhar = std_urzhar / mean_urzhar * 100

# Визуализация данных
plt.figure(figsize=(12,6))
plt.plot(data_byzhy.index, data_byzhy["flow"], label="Byzhy River")
plt.plot(data_urzhar.index, data_urzhar["flow"], label="Urzhar River")
plt.xlabel("Date")
plt.ylabel("Flow (m³/s)")
plt.legend()
plt.title("Hydrological Regimes Comparison")

# Картирование данных (необязательно)
m = folium.Map(location=[45, 80], zoom_start=7)
folium.Marker([data_byzhy.index[0].latitude, data_byzhy.index[0].longitude], popup="Byzhy River").add_to(m)
folium.Marker([data_urzhar.index[0].latitude, data_urzhar.index[0].longitude], popup="Urzhar River").add_to(m)

# Сохранение карты
m.save("204.html")

plt.show()

print(f"Mean flow Byzhy: {mean_byzhy:.2f} m³/s, CV: {cv_byzhy:.2f}%")
print(f"Mean flow Urzhar: {mean_urzhar:.2f} m³/s, CV: {cv_urzhar:.2f}%")