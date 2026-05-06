import geopandas as gpd
import folium
from shapely.geometry import Point

# Загрузить данные о гидропостах
hydroposts = gpd.read_file("path/to/hydroposts.shp")

# Определить функцию для расчета риска паводка
def risk(flow):
    if flow < 100:
        return "low"
    elif flow < 500:
        return "medium"
    else:
        return "high"

# Добавить столбец с риском паводка
hydroposts["risk"] = hydroposts["flow"].apply(risk)

# Создать карту Folium
m = folium.Map(location=[45, 60], zoom_start=12)

# Добавить гидропосты на карту
for index, row in hydroposts.iterrows():
    folium.Marker(
        location=(row["geometry"].y, row["geometry"].x),
        popup=f"Flow: {row['flow']} Risk: {row['risk']}",
        icon=folium.Icon(color=dict({"low": "green", "medium": "orange", "high": "red"})[row["risk"]])
    ).add_to(m)

# Сохранить карту
m.save("76.html")