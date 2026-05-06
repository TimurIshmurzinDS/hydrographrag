import folium
import pandas as pd

# 1. Получение данных с датчиков (пример)
data = pd.read_csv("sensors_data.csv")  

# 2. Проверка статуса датчиков (пример)
data['status'] = data['water_level'].apply(lambda x: 'исправен' if x > 1 else 'неисправен')

# 3. Визуализация результатов
m = folium.Map(location=[50.7, 14.4], zoom_start=12)  # Заменить на координаты реки Osek River

for index, row in data.iterrows():
    if row['status'] == 'исправен':
        folium.Marker([row['latitude'], row['longitude']], popup=f"Датчик {row['id']}: {row['status']}").add_to(m)
    else:
        folium.Marker([row['latitude'], row['longitude']], popup=f"Датчик {row['id']}: {row['status']}", icon=folium.Icon(color='red')).add_to(m)

# 4. Сохранение карты
m.save("68.html")