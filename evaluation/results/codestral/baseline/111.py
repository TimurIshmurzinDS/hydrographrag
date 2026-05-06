python
         import folium
         import requests
         # Загрузка данных о реках (предполагается наличие соответствующих данных)
         rivers = {
             "Aksu River": {"length": 1200, "coordinates": [41.2936, 75.805]},
             "Temirlik River": {"length": 800, "coordinates": [42.3541, 69.585]}
         }
         # Получение данных о климате (пример с использованием API OpenWeatherMap)
         api_key = "your_api_key"
         climate_data = {}
         for river, data in rivers.items():
             lat, lon = data["coordinates"]
             url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
             response = requests.get(url)
             climate_data[river] = response.json()["main"]
         # Определение индекса риска засухи (пример простого подсчета отношения температуры к длине реки)
         risk_index = {}
         for river, data in climate_data.items():
             temperature = data["temp"] - 273.15 # Конвертирование из Кельвина в Цельсий
             length = rivers[river]["length"]
             risk_index[river] = temperature / length
         # Визуализация на карте
         m = folium.Map(location=[41.5, 72], zoom_start=6)
         for river, data in rivers.items():
             color = "red" if river == max(risk_index, key=risk_index.get) else "blue"
             folium.Marker(location=data["coordinates"], popup=river, icon=folium.Icon(color=color)).add_to(m)
         m.save("111.html")