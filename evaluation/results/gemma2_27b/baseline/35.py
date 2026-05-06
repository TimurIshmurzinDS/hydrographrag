import geopandas as gpd
import folium

# Загрузка данных о реке Аягоз
river = gpd.read_file("path/to/river_Ayakoz.shp")

# Загрузка данных о расходе воды
flow_data = pd.read_csv("path/to/flow_data.csv")

# Загрузка данных о потребности в воде для ирригации
irrigation_needs = gpd.read_file("path/to/irrigation_needs.shp")

# Расчет дефицита воды
river["deficit"] = irrigation_needs["need"] - flow_data["flow"]

# Создание карты
m = folium.Map(location=[43.0, 79.0], zoom_start=8)

# Добавление линии реки на карту
folium.GeoJson(river).add_to(m)

# Визуализация дефицита воды с помощью цветовой градации
def color_function(deficit):
    if deficit < 0:
        return "green"
    elif deficit < 100:
        return "yellow"
    else:
        return "red"

river.apply(lambda row: folium.GeoJson(row["geometry"], style_function=lambda feature: {"fillColor": color_function(row["deficit"])}).add_to(m), axis=1)

# Сохранение карты
m.save("35.html")