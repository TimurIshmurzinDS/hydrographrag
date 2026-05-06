import folium
import geopandas as gpd

# Загружаем данные о постах мониторинга в формате GeoJSON
monitoring_posts = gpd.read_file("sharyn_river_monitoring_posts.geojson")

# Фильтруем посты, которые не передают данные (например, если признак "активен" равен False)
active_posts = monitoring_posts[monitoring_posts['активен'] == True]

# Если нет признака "активен", можно проверить наличие последней даты передачи данных
# active_posts = monitoring_posts[monitoring_posts['последняя_дата'].notnull()]

# Создаем карту с центром над рекой Sharyn River
m = folium.Map(location=[43.28, 69.57], zoom_start=10)

# Добавляем маркеры для неактивных постов мониторинга (красный цвет)
for index, row in active_posts.iterrows():
    if not row['активен']:
        folium.Marker([row.geometry.y, row.geometry.x], popup='Пост мониторинга', icon=folium.Icon(color='red')).add_to(m)

# Сохраняем карту в файл HTML
m.save("62.html")