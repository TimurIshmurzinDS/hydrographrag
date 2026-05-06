import pandas as pd
import folium

# Загрузка данных о расходах рек
kurty_data = pd.read_csv("kurty_river_flow.csv")
lepsy_data = pd.read_csv("lepsy_river_flow.csv")

# Суммирование объемов воды из обеих рек
total_water_volume = kurty_data["flow"].sum() + lepsy_data["flow"].sum()

# Загрузка данных о сельскохозяйственном спросе
agricultural_demand = pd.read_csv("agricultural_demand.csv")

# Сравнение доступных объемов воды с需求
if total_water_volume >= agricultural_demand:
    print("Достаточно воды для удовлетворения сельскохозяйственного спроса.")
else:
    print("Недостаточно воды для удовлетворения сельскохозяйственного спроса.")

# Визуализация (необязательно)
m = folium.Map(location=[45, 60], zoom_start=8)
folium.GeoJson("rivers.geojson").add_to(m)
m.save("120.html")