import pandas as pd
import folium

# Загрузка данных о мониторинге рек
data = pd.read_csv("river_monitoring_data.csv")

# Определение критических уровней (замените на актуальные данные)
critical_levels = {
    "River A": 10,
    "River B": 5,
    "River C": 8
}

# Сравнение текущих уровней с критическими и выделение рек с критическим уровнем
critical_rivers = data[data["Water Level"] > critical_levels.get(data["River Name"])]

# Создание карты (optional)
m = folium.Map()

for index, row in critical_rivers.iterrows():
    folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=f"{row['River Name']} - {row['Water Level']}").add_to(m)

# Сохранение карты
m.save("141.html")