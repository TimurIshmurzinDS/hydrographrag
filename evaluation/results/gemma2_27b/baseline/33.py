import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных о расходе воды в реке Аксу (пример)
water_flow = pd.read_csv("aksu_water_flow.csv") 

# Загрузка данных о зонах сельскохозяйственного использования
agriculture_zones = gpd.read_file("agriculture_zones.shp")

# Расчет объема воды для каждой зоны (пример)
agriculture_zones["water_volume"] = agriculture_zones.area * 0.5  # Примерный коэффициент орошения

# Суммирование объемов воды
total_water_volume = agriculture_zones["water_volume"].sum()

# Визуализация на карте (пример)
m = folium.Map(location=[42.87, 70.5], zoom_start=10)
folium.GeoJson(agriculture_zones).add_to(m)
m.save("33.html")

print(f"Общий объем воды, забираемый на нужды сельского хозяйства из реки Аксу: {total_water_volume} м³")