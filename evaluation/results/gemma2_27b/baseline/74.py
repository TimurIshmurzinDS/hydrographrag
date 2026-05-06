import pandas as pd
import folium

# Загрузить данные о показаниях сенсоров
data = pd.read_csv("sensor_data.csv")

# Вычислить среднее значение и стандартное отклонение
mean = data["value"].mean()
std = data["value"].std()

# Определить порог аномалий (три сигмы)
threshold = mean + 3 * std

# Найти аномальные значения
anomalous_values = data[data["value"] > threshold]

# Создать карту с помощью Folium
m = folium.Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=12)

# Добавить сенсоры на карту
for index, row in data.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Value: {row['value']}", color="green").add_to(m)

# Выделить аномальные значения красным цветом
for index, row in anomalous_values.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Anomalous Value: {row['value']}", color="red").add_to(m)

# Сохранить карту
m.save("74.html")