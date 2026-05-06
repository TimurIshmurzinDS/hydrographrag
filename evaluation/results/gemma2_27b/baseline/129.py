import pandas as pd
import matplotlib.pyplot as plt
import folium

# **1. Получение данных:**

# Заменить "data.csv" на актуальный файл с данными о расходе воды
df = pd.read_csv("data.csv")

# **2. Обработка данных:**

# Фильтруем данные по периоду весеннего половодья (заменить даты на актуальные)
df_spring = df[(df["date"] >= "2019-03-01") & (df["date"] <= "2019-05-31")]

# **3. Сравнение показателей:**

# Рассчитываем средний расход воды за каждый год
yearly_average = df_spring.groupby(["year"]).mean()["discharge"]

# Визуализируем данные с помощью matplotlib
plt.bar(yearly_average.index, yearly_average.values)
plt.xlabel("Год")
plt.ylabel("Средний расход воды (м³/с)")
plt.title("Сравнение расхода воды в Kurty и Tekes за весеннее половодье")

# **4. Картографирование:**

# Создаем карту с помощью folium
m = folium.Map(location=[50, 60], zoom_start=8)

# Добавляем точки на карте (заменить координаты на актуальные)
folium.Marker([50.1, 60.2], popup="Kurty River").add_to(m)
folium.Marker([50.3, 60.4], popup="Tekes River").add_to(m)

# Сохраняем карту
m.save("129.html")

plt.show()