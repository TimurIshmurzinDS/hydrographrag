import pandas as pd
from folium import Map, Marker

# Загрузка данных о расходе воды (замените на путь к вашему файлу)
data = pd.read_csv("batareyka_flow_data.csv")

# Преобразование даты в формат datetime
data["Date"] = pd.to_datetime(data["Date"])

# Фильтрация данных по периоду весеннего таяния (замените на соответствующие даты)
spring_melt_data = data[(data["Date"] >= "2023-03-15") & (data["Date"] <= "2023-05-15")]

# Интерполяция значений расхода воды (если необходимо)

# Создание карты
m = Map(location=[55.75, 37.62], zoom_start=12)  # Замените на координаты реки Batareyka

# Добавление маркеров с значениями расхода воды
for index, row in spring_melt_data.iterrows():
    Marker(location=[row["Latitude"], row["Longitude"]], popup=f"Расход: {row['Flow']} м³/с").add_to(m)

# Сохранение карты
m.save("27.html")