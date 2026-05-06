import pandas as pd
import folium

# Загрузка данных о расходе воды
tekes_data = pd.read_csv("tekes_river_flow.csv", parse_dates=["date"])
bayankol_data = pd.read_csv("bayankol_river_flow.csv", parse_dates=["date"])

# Вычисление среднего дневного расхода воды
tekes_avg_flow = tekes_data.groupby(tekes_data["date"].dt.date)["flow"].mean()
bayankol_avg_flow = bayankol_data.groupby(bayankol_data["date"].dt.date)["flow"].mean()

# Создание карты
m = folium.Map(location=[48.0, 85.0], zoom_start=6)  # Примерные координаты

# Добавление точек рек на карту
folium.Marker([48.1234, 85.5678], popup="Tekes River").add_to(m)
folium.Marker([47.8901, 84.3210], popup="Bayankol River").add_to(m)

# Добавление графиков расхода воды
folium.plugins.TimeSeriesChart(
    data={"Tekes River": tekes_avg_flow.values.tolist(), "Bayankol River": bayankol_avg_flow.values.tolist()},
    name="River Flow",
).add_to(m)

# Сохранение карты
m.save("25.html")