import pandas as pd
import numpy as np
import folium
from branca.colormap import LinearColormap

# Шаг 1: Сбор данных о гидрологическом режиме реки Шарын
# Предположим, что у нас есть данные в формате CSV с уровнями воды и скоростями течения.
hydro_data = pd.read_csv('sharyn_hydro_data.csv')  # Пример файла с данными

# Шаг 2: Анализ текущего состояния туризма
# Предположим, что у нас есть данные о туристических маршрутах и популярных местах.
tourism_data = pd.read_csv('sharyn_tourism_data.csv')  # Пример файла с данными

# Шаг 3: Моделирование изменений гидрологического режима
# Для простоты предположим, что мы используем линейную регрессию для прогнозирования уровня воды.
from sklearn.linear_model import LinearRegression

X = hydro_data[['year']]
y = hydro_data['water_level']

model = LinearRegression()
model.fit(X, y)

future_years = np.array([[2030], [2040], [2050]])
predicted_levels = model.predict(future_years)

# Шаг 4: Оценка влияния на туризм
# Предположим, что уровень воды напрямую влияет на популярность туристических маршрутов.
# Если уровень воды выше определенного порога, то поток туристов может уменьшиться.

threshold = np.mean(y)
tourism_data['predicted_water_level'] = tourism_data['year'].apply(lambda x: model.predict([[x]])[0])
tourism_data['impact_on_tourism'] = tourism_data['predicted_water_level'].apply(lambda x: 1 if x < threshold else -1)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[49.8326, 73.093], zoom_start=10)  # Координаты примерного центра региона

colormap = LinearColormap(['green', 'red'], vmin=-1, vmax=1)
for _, row in tourism_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=colormap(row['impact_on_tourism']),
        fill=True,
        fill_color=colormap(row['impact_on_tourism'])
    ).add_to(m)

folium.LayerControl().add_to(m)
m.save("194.html")