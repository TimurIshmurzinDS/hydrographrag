import pandas as pd
import folium

# Загрузка данных
data = pd.read_csv('monitoring_data.csv')

# Проверка наличия аномалий в данных
# Пример: проверка на отсутствие значений
anomalies = data[data.isnull().any(axis=1)]

if not anomalies.empty:
    print("Обнаружены аномалии:")
    print(anomalies)
else:
    print("Аномалий не обнаружено.")

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление маркеров на карте
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"ID: {row['id']}, State: {row['state']}",
        icon=folium.Icon(color='red' if row['state'] == 'offline' else 'green')
    ).add_to(m)

# Сохранение карты
m.save("142.html")