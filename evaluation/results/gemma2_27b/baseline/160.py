import pandas as pd
import folium

# Загрузка данных о расходе воды
data_ili = pd.read_csv("data_ili.csv")
data_shyzhyn = pd.read_csv("data_shyzhyn.csv")

# Расчет средних значений по месяцам
monthly_averages_ili = data_ili.groupby(pd.Grouper(key="date", freq="M")).mean()
monthly_averages_shyzhyn = data_shyzhyn.groupby(pd.Grouper(key="date", freq="M")).mean()

# Создание карты
m = folium.Map(location=[43, 78], zoom_start=6)

# Визуализация данных Ili River
folium.GeoJson("ili_river.geojson").add_to(m)
for index, row in monthly_averages_ili.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=5, color="red" if row["mean_flow"] > 10 else "blue", fill=True).add_to(m)

# Визуализация данных Shyzhyn River
folium.GeoJson("shyzhyn_river.geojson").add_to(m)
for index, row in monthly_averages_shyzhyn.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=5, color="red" if row["mean_flow"] > 10 else "blue", fill=True).add_to(m)

# Сохранение карты
m.save("160.html")