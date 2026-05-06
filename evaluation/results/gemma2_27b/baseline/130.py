import pandas as pd
import folium

# Загрузка данных
bayankol_data = pd.read_csv("bayankol_flow.csv")
shilik_data = pd.read_csv("shilik_flow.csv")

# Расчет отклонения
deviation = bayankol_data["flow"] - shilik_data["flow"]

# Создание карты
m = folium.Map(location=[45, 80], zoom_start=7)

# Добавление точек на карту с информацией о отклонении
for i in range(len(deviation)):
    folium.Marker(
        location=[bayankol_data["latitude"][i], bayankol_data["longitude"][i]],
        popup=f"Отклонение: {deviation[i]}",
    ).add_to(m)

# Сохранение карты
m.save("130.html")