import folium
import pandas as pd

# Шаг 1: Получение данных о потреблении воды
data = pd.read_csv('water_consumption_data.csv')

# Шаг 2: Подготовка данных
# Предполагается, что данные уже очищены и готовы к использованию

# Шаг 3: Геокодирование адресов (если необходимо)
# addresses = data['address']
# locations = geolocate_addresses(addresses)

# Шаг 4: Визуализация данных
m = folium.Map(location=[51.2879, 65.9038], zoom_start=8) # Координаты реки Аксу

for index, row in data.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    consumption = row['consumption']

    # Используем размер точек для представления уровня потребления воды
    popup_text = f'Потребление воды: {consumption} куб. м'
    folium.CircleMarker(location=[lat, lon], radius=consumption/1000, fill=True, fill_opacity=0.5).add_to(m)
    folium.Marker([lat, lon], popup=folium.Popup(popup_text)).add_to(m)

# Шаг 5: Сохранение карты
m.save("41.html")