import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from folium import Map, FeatureGroup, GeoJson


# Загрузить данные о потреблении воды из CSV файла
water_data = pd.read_csv("water_consumption.csv")

# Загрузить данные о урожайности из CSV файла
yield_data = pd.read_csv("crop_yields.csv")

# Объединить данные по году
merged_data = pd.merge(water_data, yield_data, on="Year")

# Вычислить коэффициент корреляции для каждой культуры
for crop in merged_data["Crop"].unique():
    correlation, p_value = pearsonr(merged_data[merged_data["Crop"] == crop]["Water Consumption"], 
                                    merged_data[merged_data["Crop"] == crop]["Yield"])

    print(f"Correlation between water consumption and yield for {crop}: {correlation}")

# Создать график для визуализации данных
plt.scatter(merged_data["Water Consumption"], merged_data["Yield"])
plt.xlabel("Water Consumption")
plt.ylabel("Yield")
plt.show()

# Создать карту с Folium
m = Map(location=[45, 60], zoom_start=8)

# Добавить данные о реке на карту (в формате GeoJSON)
river_data = pd.read_csv("river_data.geojson")
folium.GeoJson(data=river_data).add_to(m)

# Сохранить карту в HTML файл
m.save("185.html")