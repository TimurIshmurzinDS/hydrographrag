import folium

# Заменить на реальные данные о датчиках
sensors = [
    {"name": "Sensor 1", "river": "Osek River", "latitude": 53.25, "longitude": 48.50, "status": "working"},
    {"name": "Sensor 2", "river": "Koktal River", "latitude": 53.10, "longitude": 49.00, "status": "not working"},
    # ... добавить остальные датчики
]

m = folium.Map(location=[53.20, 48.75], zoom_start=10)

for sensor in sensors:
    color = "green" if sensor["status"] == "working" else "red"
    folium.Marker(location=[sensor["latitude"], sensor["longitude"]], popup=f"{sensor['name']} ({sensor['river']})", icon=folium.Icon(color=color)).add_to(m)

m.save("73.html")