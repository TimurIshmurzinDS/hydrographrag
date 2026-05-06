import pandas as pd
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных (замените на ваши файлы)
data_koksu = pd.read_csv("koksu_river_flow.csv", index_col="date")
data_emel = pd.read_csv("emel_river_flow.csv", index_col="date")

# 2. Обработка данных (преобразование индекса в формат datetime)
data_koksu.index = pd.to_datetime(data_koksu.index)
data_emel.index = pd.to_datetime(data_emel.index)

# 3. Расчет среднемесячных значений
monthly_mean_koksu = data_koksu.resample("M").mean()
monthly_mean_emel = data_emel.resample("M").mean()

# 4. Визуализация данных
plt.figure(figsize=(12,6))
plt.plot(monthly_mean_koksu["flow"], label="Koksu River")
plt.plot(monthly_mean_emel["flow"], label="Emel River")
plt.xlabel("Month")
plt.ylabel("Flow (m³/s)")
plt.legend()
plt.title("Seasonal Flow Patterns in Koksu and Emel Rivers")

# 5. Картографирование (необязательно)
m = folium.Map(location=[43.2, 78.0], zoom_start=8)
folium.Marker([43.2, 78.0], popup="Koksu River").add_to(m)
folium.Marker([43.5, 79.0], popup="Emel River").add_to(m)

# 6. Сохранение карты (необязательно)
m.save("196.html")

plt.show()