import pandas as pd
import folium

# Загрузка данных о постах на реке Karaoy River
posts_data = pd.read_csv('path_to_posts_data.csv')

# Загрузка данных о критических отметках паводка
flood_data = pd.read_csv('path_to_flood_data.csv')

# Фильтрация данных о постах, чтобы получить только те, которые находятся на реке Karaoy River
karaoy_posts = posts_data[posts_data['river'] == 'Karaoy']

# Проверка превышения критической отметки для каждого фильтрованного поста
karaoy_posts['exceeds_critical'] = karaoy_posts.apply(lambda row: row['flow_rate'] > flood_data[flood_data['station'] == row['station']]['critical_level'].values[0], axis=1)

# Визуализация данных на карте
m = folium.Map(location=[karaoy_posts['latitude'].mean(), karaoy_posts['longitude'].mean()], zoom_start=12)

for index, row in karaoy_posts.iterrows():
    if row['exceeds_critical']:
        color = 'red'
    else:
        color = 'green'
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Station: {row['station']}, Flow Rate: {row['flow_rate']}, Exceeds Critical: {row['exceeds_critical']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("82.html")