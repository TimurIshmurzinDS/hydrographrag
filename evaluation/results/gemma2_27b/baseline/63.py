import geopandas as gpd
import folium

# Загрузка данных о гидропостах (замените на актуальные пути к файлам)
hydroposts = gpd.read_file("hydroposts_byzhy.shp")

# Загрузка данных об уровнях воды (замените на актуальный источник данных)
water_levels = pd.read_csv("water_levels_byzhy.csv")

# Объединение данных по ID гидропоста
merged_data = hydroposts.merge(water_levels, on="hydropost_id")

# Создание карты с folium
m = folium.Map(location=[merged_data["geometry"].y.mean(), merged_data["geometry"].x.mean()], zoom_start=12)

# Добавление маркеров на карту с уровнями воды
for index, row in merged_data.iterrows():
    folium.Marker(
        location=[row["geometry"].y, row["geometry"].x],
        popup=f"Уровень воды: {row['water_level']} м",
    ).add_to(m)

# Сохранение карты
m.save("63.html")