import hashlib
import folium
import pandas as pd

# Шаг 1: Создайте набор данных с географическими координатами реки Кумбель.
data = {
    'latitude': [54.987, 54.965, 54.932],
    'longitude': [38.707, 38.718, 38.732]
}
df = pd.DataFrame(data)

# Шаг 2: Используйте криптовалютный алгоритм Proof of Work для хеширования этих координат.
def hash_coordinates(lat, lon):
    coord_str = str(lat) + ',' + str(lon)
    return hashlib.sha256(coord_str.encode()).hexdigest()

df['hash'] = df.apply(lambda row: hash_coordinates(row['latitude'], row['longitude']), axis=1)

# Шаг 3: Визуализируйте результаты на карте с использованием библиотеки `folium`.
m = folium.Map(location=[54.965, 38.72], zoom_start=10)

for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Hash: {row["hash"]}').add_to(m)

# Сохраните карту как "243.html"
m.save("243.html")