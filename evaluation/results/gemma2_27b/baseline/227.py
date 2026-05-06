import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных о расходе реки Или (в м³/с)
data = pd.read_csv("ili_river_flow.csv", index_col="Date")

# Расчет потребления энергии для майнинга одного биткоина (в kWh)
energy_consumption = 10000  # Пример: 10000 kWh

# Определение периода наибольшего расхода реки
max_flow = data["Flow"].idxmax()

# Создание карты с местоположением реки Или
m = folium.Map(location=[43.2, 78.5], zoom_start=8)

# Добавление линии реки на карту
folium.GeoJson("ili_river_geojson.geojson").add_to(m)

# Добавление маркера с максимальным расходом
folium.Marker(location=[43.2, 78.5], popup="Max Flow: " + str(data["Flow"].max())).add_to(m)

# Сохранение карты
m.save("227.html")

# Вывод данных о максимальном расходе и времени
print("Maximum River Flow:", data["Flow"].max())
print("Date of Maximum Flow:", max_flow)

# Пример функции для запуска майнинга в зависимости от сезона
def start_mining():
    if data["Flow"][pd.to_datetime(data.index)] > 100:  # Пример порог расхода
        print("Starting mining...")
    else:
        print("Waiting for optimal conditions.")