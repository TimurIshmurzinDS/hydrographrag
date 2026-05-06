import folium
import pandas as pd

# Загрузка данных о сенсорах (пример)
data = {
    'id': [1, 2, 3, 4],
    'latitude': [59.8670, 59.8720, 59.8780, 59.8840],
    'longitude': [-154.7390, -154.7440, -154.7490, -154.7540],
    'status': ['активный', 'ошибка', 'неактивный', 'активный']
}
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[59.8750, -154.7450], zoom_start=16)

# Добавление маркеров для сенсоров на карту
for _, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"ID: {row['id']}, Статус: {row['status']}").add_to(m)

# Сохранение карты в файл HTML
m.save("64.html")