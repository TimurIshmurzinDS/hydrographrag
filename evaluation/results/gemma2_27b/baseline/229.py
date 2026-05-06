import geopandas as gpd
import folium

# Загрузить данные о зоне риска наводнения
risk_zone = gpd.read_file("path/to/risk_zone.shp")

# Определить координаты места приготовления борща
borch_location = (43.25, 76.91)

# Вычислить расстояние до ближайшей точки риска
distance_to_risk = risk_zone.geometry.apply(lambda x: x.distance(gpd.GeoSeries([Point(borch_location)]).iloc[0]))
closest_point = distance_to_risk.idxmin()

# Создать индикатор риска
risk_indicator = 1 / (distance_to_closest_point + 1)

# Базовый рецепт борща
base_recipe = {
    "мясо": "500 г",
    "картофель": "3 шт.",
    "морковь": "2 шт.",
    "свекла": "1 шт.",
    "капуста": "1/4 кочана",
}

# Адаптация рецепта в зависимости от риска
if risk_indicator < 0.2:
    recipe = base_recipe
elif 0.2 <= risk_indicator < 0.5:
    recipe = {**base_recipe, "сушеные грибы": "50 г"}
else:
    recipe = {"консервированный борщ": "1 банка"}

# Визуализация на карте
m = folium.Map(location=borch_location, zoom_start=12)
folium.GeoJson(risk_zone).add_to(m)
folium.Marker(location=borch_location, popup="Место приготовления борща").add_to(m)

m.save("229.html")