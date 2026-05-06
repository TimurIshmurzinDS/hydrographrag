import pandas as pd
import folium

# Загрузить данные о расходах рек
baskan_data = pd.read_csv("baskan_river_data.csv")
prokhodnaya_data = pd.read_csv("prokhodnaya_river_data.csv")

# Выделить столбцы с информацией о расходах и дате
baskan_flows = baskan_data["flow"]
prokhodnaya_flows = prokhodnaya_data["flow"]
dates = baskan_data["date"]

# Вычислить разницу в расходах
difference = baskan_flows - prokhodnaya_flows

# Создать карту с помощью folium
m = folium.Map(location=[45, 60], zoom_start=8)

# Добавить реки на карту (необходимо получить координаты рек из данных)
folium.GeoJson("baskan_river_coordinates.geojson", name="Baskan River").add_to(m)
folium.GeoJson("prokhodnaya_river_coordinates.geojson", name="Prokhodnaya River").add_to(m)

# Визуализировать разницу расходов цветом или размером линий (необходимо добавить код для этого шага)

# Сохранить карту
m.save("89.html")