import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и их уровнях воды
water_level_data = {
    "Sarykan River": [
        {"Date_water_level_Value": "2023-10-01", "Water_level_Valuecm": 50},
        {"Date_water_level_Value": "2023-10-02", "Water_level_Valuecm": 60},
        {"Date_water_level_Value": "2023-10-03", "Water_level_Valuecm": 70},
        {"Date_water_level_Value": "2023-10-04", "Water_level_Valuecm": 80},  # Аномальный показатель
        {"Date_water_level_Value": "2023-10-05", "Water_level_Valuecm": 90},
    ]
}

# Загрузка границы бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs(epsg=4326, inplace=True)

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Фильтрация данных для реки Сарыкан и проверка аномальных показателей
anomalous_rivers = []
for river, data in water_level_data.items():
    for entry in data:
        if river == "Sarykan River" and entry["Water_level_Valuecm"] > 75:  # Порог для аномального уровня воды
            anomalous_rivers.append(river)
            break

# Визуализация аномальных рек на карте
if anomalous_rivers:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup="Аномальные показатели уровня воды в реке Сарыкан",
        icon=folium.Icon(color='red', icon='warning')
    ).add_to(m)

# Сохранение карты
m.save("139.html")