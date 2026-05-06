import geopandas as gpd
import folium
from shapely.geometry import Point

# Загрузка данных (пример)
hydrology_data = gpd.read_file("hydrology_data.shp")
water_consumption_points = gpd.read_file("water_consumption_points.shp")
ecosystem_data = gpd.read_file("ecosystem_data.shp")

# Анализ гидрологического режима (пример)
average_flow = hydrology_data["flow"].mean()
print(f"Средний расход воды в реке: {average_flow}")

# Моделирование воздействия (пример)
for index, row in water_consumption_points.iterrows():
    consumption = row["consumption"]
    location = Point(row["longitude"], row["latitude"])
    # ... (модель для оценки влияния потребления на экосистему)

# Визуализация результатов
m = folium.Map(location=[water_consumption_points["latitude"].mean(), water_consumption_points["longitude"].mean()], zoom_start=10)

for index, row in water_consumption_points.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Потребление: {row['consumption']}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

# ... (добавление данных об экосистеме и гидрологическом режиме на карту)

m.save("36.html")