import geopandas as gpd
import folium

# Загрузка данных о постах мониторинга
posts = gpd.read_file("sharyn_river_monitoring_posts.shp")

# Загрузка данных о статусе передачи данных
data_status = pd.read_csv("data_status.csv")

# Объединение данных по ID поста
merged_data = posts.merge(data_status, on="post_id")

# Фильтрация постов без данных
no_data_posts = merged_data[merged_data["data_status"] == "не передаёт"]

# Создание карты
m = folium.Map(location=[43.0, 78.0], zoom_start=10)

# Добавление маркеров постов без данных на карту
for index, row in no_data_posts.iterrows():
    folium.Marker(
        location=[row["geometry"].y, row["geometry"].x],
        popup=f"Пост ID: {row['post_id']}",
        icon=folium.Icon(color="red", icon="warning-sign"),
    ).add_to(m)

# Сохранение карты
m.save("62.html")