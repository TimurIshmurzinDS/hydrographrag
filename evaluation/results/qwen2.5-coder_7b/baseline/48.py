import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример функции для загрузки данных (замените на реальный источник данных)
def load_water_flow_data():
    # Здесь должна быть реализована логика для загрузки данных о расходе воды
    # Например, из CSV файла или API
    data = {
        'date': pd.date_range(start='2010-01-01', end='2020-12-31'),
        'flow_rate': [100 + i * 5 for i in range(4380)]  # Пример данных
    }
    return pd.DataFrame(data)

# Загрузка данных о расходе воды
water_flow_data = load_water_flow_data()

# Преобразование данных в формат для визуализации на карте
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in water_flow_data.iterrows():
    date_str = row['date'].strftime('%Y-%m-%dT%H:%M:%SZ')
    flow_rate = row['flow_rate']
    geojson_data["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [35.0, 41.0]  # Пример координат (замените на реальные)
        },
        "properties": {
            "time": date_str,
            "flow_rate": flow_rate
        }
    })

# Создание карты
m = folium.Map(location=[41.0, 35.0], zoom_start=6)

# Добавление слоя с временной геоданныей
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("48.html")

print("Карта сохранена как 48.html")