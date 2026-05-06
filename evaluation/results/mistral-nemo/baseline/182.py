import folium
import geopandas as gpd

# 1. Сбор данных
rainfall_data = {"average_annual_rainfall": ..., "catchment_area": ...}
agriculture_data = {"agricultural_area": ..., "water_consumption_norm": ..., "total_water_demand": ...}

# 2. Оценка водных ресурсов
total_water_supply = rainfall_data["average_annual_rainfall"] * rainfall_data["catchment_area"]

# 3. Оценка потребности сельского хозяйства в воде
total_water_demand = agriculture_data["agricultural_area"] * agriculture_data["water_consumption_norm"]

# 4. Анализ рисков дефицита воды
if total_water_supply < total_water_demand:
    risk_level = "High"
elif total_water_supply <= total_water_demand and total_water_supply >= (total_water_demand * 0.8):
    risk_level = "Medium"
else:
    risk_level = "Low"

# 5. Визуализация результатов
m = folium.Map(location=[..., ], zoom_start=...)
gdf = gpd.read_file("catchment_shapefile.shp")
gdf["risk_level"] = risk_level
for _, row in gdf.iterrows():
    folium.geo_json(row.geometry, style_function=lambda x: {"fillColor": "green" if row.risk_level == "Low" else ("yellow" if row.risk_level == "Medium" else "red"), "color": "black", "weight": 2}).add_to(m)

m.save("182.html")