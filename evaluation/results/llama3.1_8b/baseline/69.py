import pandas as pd
import folium

# Загрузим данные о местоположении датчиков на обеих реках в DataFrames
koktal_data = pd.DataFrame({
    'id': [1, 2, 3],
    'latitude': [43.1234, 43.4567, 43.7890],
    'longitude': [79.0123, 79.3456, 79.6789]
})

aksu_data = pd.DataFrame({
    'id': [1, 2, 3],
    'latitude': [44.1234, 44.4567, 44.7890],
    'longitude': [80.0123, 80.3456, 80.6789]
})

# Получим актуальные данные о статусе датчиков (для примера)
koktal_status = pd.DataFrame({
    'id': [1, 2, 3],
    'temperature': [15, 20, 18],
    'water_level': [10, 12, 11]
})

aksu_status = pd.DataFrame({
    'id': [1, 2, 3],
    'temperature': [16, 22, 19],
    'water_level': [9, 13, 12]
})

# Создадим географическую карту с маркерами для каждого датчика на обеих реках
m = folium.Map(location=[43.5, 79.5], zoom_start=10)

for index, row in koktal_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f'Датчик {row["id"]}: Температура - {koktal_status.loc[koktal_status["id"] == row["id"], "temperature"].values[0]}°C, Уровень воды - {koktal_status.loc[koktal_status["id"] == row["id"], "water_level"].values[0]}').add_to(m)

for index, row in aksu_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f'Датчик {row["id"]}: Температура - {aksu_status.loc[aksu_status["id"] == row["id"], "temperature"].values[0]}°C, Уровень воды - {aksu_status.loc[aksu_status["id"] == row["id"], "water_level"].values[0]}').add_to(m)

# Сравним статус датчиков на обеих реках и выявим любые различия
koktal_diff = pd.merge(koktal_data, koktal_status, on='id')
aksu_diff = pd.merge(aksu_data, aksu_status, on='id')

print("Различия в статусе датчиков на реке Koktal River:")
print(koktal_diff[koktal_diff['temperature'] != koktal_diff['temperature_y']].head())

print("\nРазличия в статусе датчиков на реке Aksu River:")
print(aksu_diff[aksu_diff['temperature'] != aksu_diff['temperature_y']].head())

# Сохраним карту как HTML-файл
m.save("69.html")