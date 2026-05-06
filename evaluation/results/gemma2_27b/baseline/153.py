import geopandas as gpd
import folium

# Загрузить данные о речной сети
rivers = gpd.read_file("sarykan_rivers.shp")

# Загрузить данные о гидрологическом режиме (например, CSV)
hydrology = pd.read_csv("river_flows.csv")

# Объединить данные о реках и гидрологическом режиме
rivers = rivers.merge(hydrology, on="river_name")

# Вычислить показатель подверженности весенним половодьям
rivers["flood_susceptibility"] = rivers["max_spring_flow"] / rivers["mean_annual_flow"]

# Создать карту с использованием Folium
m = folium.Map(location=[43.2, 78.5], zoom_start=10)

# Добавить реки на карту, раскрашенные в зависимости от подверженности весенним половодьям
for index, row in rivers.iterrows():
    folium.GeoJson(data=row.geometry, style_function=lambda feature: {
        "color": "green" if row["flood_susceptibility"] < 1.5 else "yellow" if row["flood_susceptibility"] < 2 else "red",
        "weight": 3
    }).add_to(m)

# Сохранить карту
m.save("153.html")