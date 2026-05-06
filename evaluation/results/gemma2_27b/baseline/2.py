import requests
import folium

# Замените на реальный URL API или источник данных
api_url = 'https://example.com/api/water-sensors' 

response = requests.get(api_url)
data = response.json()

# Найдите датчик на реке Каратал по ID или названию
karatal_sensor = next((sensor for sensor in data if sensor['river'] == 'Каратал'), None)

if karatal_sensor:
    status = karatal_sensor['status']
    latitude = karatal_sensor['latitude']
    longitude = karatal_sensor['longitude']

    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Определите цвет маркера в зависимости от статуса
    if status == 'работающий':
        color = 'green'
    elif status == 'неисправный':
        color = 'red'
    else:
        color = 'gray'

    folium.Marker(
        location=[latitude, longitude],
        popup=f"Статус датчика: {status}",
        icon=folium.Icon(color=color)
    ).add_to(m)

    m.save("2.html")
else:
    print("Датчик на реке Каратал не найден.")