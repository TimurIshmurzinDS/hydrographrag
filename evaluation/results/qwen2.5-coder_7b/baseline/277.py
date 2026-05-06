import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: год, компания, доход
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
             2021, 2022, 2023],
    'Company': ['TechA', 'TechB', 'TechC'] * 4,
    'Revenue': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600,
                650, 700, 750]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Группировка данных по году и вычисление средней прибыльности
grouped_df = df.groupby('Year')['Revenue'].mean().reset_index()

# Создание карты
m = folium.Map(location=[48.8566, 2.3522], zoom_start=2)

# Формирование данных для визуализации на карте
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in grouped_df.iterrows():
    geojson_data["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['Year'], row['Revenue']]
        },
        "properties": {
            "time": f"{int(row['Year'])}-01-01T00:00:00Z",
            "Company": "Tech Sector",
            "Revenue": int(row['Revenue'])
        }
    })

# Добавление слоя с временной геоданныей
TimestampedGeoJson(geojson_data, period="P1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("277.html")