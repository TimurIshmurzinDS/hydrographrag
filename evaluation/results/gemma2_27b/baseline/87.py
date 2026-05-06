import pandas as pd
import folium

# 1. Получение данных
current_data = pd.read_csv("current_flow_data.csv")
historical_data = pd.read_csv("historical_flood_data.csv")

# 2. Обработка данных
current_data["date"] = pd.to_datetime(current_data["date"])
historical_data["date"] = pd.to_datetime(historical_data["date"])

# 3. Сравнение данных
average_flood_flow = historical_data[historical_data["month"] == "March"]["flow"].mean()
current_flow = current_data["flow"][0]

# 4. Визуализация
m = folium.Map(location=[56.8, 37.2], zoom_start=12)

folium.GeoJson("river_shapefile.geojson", name="Prokhodnaya River").add_to(m)

if current_flow > average_flood_flow:
    color = "red"
else:
    color = "green"

folium.Marker(location=[56.8, 37.2], popup=f"Current Flow: {current_flow} m³/s", icon=folium.Icon(color=color)).add_to(m)

m.save("87.html")