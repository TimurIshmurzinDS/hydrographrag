import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о выбросах сточных вод
wastewater_outfalls = gpd.read_file("wastewater_outfalls.shp")

# Загрузка гидрологической модели реки Талгар
talgar_river = gpd.read_file("talgar_river.shp")

# Определение параметров загрязнения (пример)
pollutants = {"BOD": 10, "COD": 20}  # Концентрации в мг/л

# Моделирование распространения загрязнения (псевдокод)
# ...

# Расчет уровня загрязнения по стандартам качества воды

# Создание карты с folium
m = folium.Map(location=[43.25, 76.9], zoom_start=12)

# Визуализация результатов на карте
for index, row in wastewater_outfalls.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"BOD: {pollutants['BOD']} mg/l<br>COD: {pollutants['COD']} mg/l",
        icon=folium.Icon(color="red"),
    ).add_to(m)

# Сохранение карты
m.save("40.html")