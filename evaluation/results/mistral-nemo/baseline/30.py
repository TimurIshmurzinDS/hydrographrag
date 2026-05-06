import folium
import pandas as pd

# Шаг 1: Подготовка данных
data = {
    'River': ['Prokhodnaya River'],
    'Current_flow': [500],  # в м³/с
    'Catchment_area': [2500],  # в км²
    'Average_slope': [0.03],  # средний уклон реки в градусах
    'Population_density': [100],  # плотность населения вдоль реки в чел./км²
    'Protection_structures': [True]  # наличие защитных сооружений (True/False)
}

df = pd.DataFrame(data)

# Шаг 2: Вычисление индекса риска наводнения
def flood_risk_index(row):
    current_flow = row['Current_flow']
    catchment_area = row['Catchment_area']
    average_slope = row['Average_slope']
    population_density = row['Population_density']
    protection_structures = row['Protection_structures']

    risk_index = (current_flow / catchment_area) * average_slope * population_density / protection_structures

    return risk_index

df['Flood_Risk_Index'] = df.apply(flood_risk_index, axis=1)

# Шаг 3: Визуализация результатов
m = folium.Map(location=[54.7355, 39.2083], zoom_start=10)  # координаты реки Прокходная

for index, row in df.iterrows():
    river_name = row['River']
    risk_index = row['Flood_Risk_Index']

    folium.CircleMarker(
        location=[54.7355, 39.2083],  # координаты реки Прокходная
        radius=risk_index/10,
        color='red' if risk_index > 0.5 else 'green',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("30.html")