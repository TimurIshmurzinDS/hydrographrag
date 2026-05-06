import pandas as pd
import folium

# Сбор данных о показателях загрязнения воды в реке Лепси (предположим, что данные хранятся в DataFrame)
data = {
    'Latitude': [55.7833, 55.7333, 55.6833],
    'Longitude': [21.2833, 21.2333, 21.1833],
    'Parameter': ['pH', 'Temperature', 'Nitrogen'],
    'Value': [7.2, 12.5, 10.8]
}
df = pd.DataFrame(data)

# Создание географической карты с указанием местоположения реки Лепси
m = folium.Map(location=[55.7833, 21.2833], zoom_start=12)

# Добавление на карте точек, представляющих места измерения показателей загрязнения воды
for i in range(len(df)):
    folium.Marker(
        location=[df.loc[i, 'Latitude'], df.loc[i, 'Longitude']],
        popup=f"Показатель: {df.loc[i, 'Parameter']}\nЗначение: {df.loc[i, 'Value']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Анализ и визуализация данных о показателях загрязнения воды
m.save("34.html")