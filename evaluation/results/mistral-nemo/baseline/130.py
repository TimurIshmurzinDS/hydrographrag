import pandas as pd
import folium

# 1. Подготовка данных
bayankol_data = pd.read_csv('bayankol_stok.csv')
shilik_data = pd.read_csv('shilik_base_level.csv')

# 2. Преобразование данных
bayankol_series = pd.Series(bayankol_data['stok'])
shilik_series = pd.Series(shilik_data['base_level'])

# 3. Расчет отклонений
deviations = bayankol_series - shilik_series

# 4. Визуализация результатов
m = folium.Map(location=[bayankol_data['latitude'].mean(), bayankol_data['longitude'].mean()], zoom_start=10)

for idx, row in bayankol_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=deviations[idx] * 2,
        color='blue',
        fill=True
    ).add_to(m)

# 5. Сохранение результатов
m.save("130.html")