import pandas as pd
from sklearn.neural_network import MLPRegressor
import folium

# Шаг 1: Подготовка данных
rainfall_data = pd.read_csv('rainfall_data.csv')
dose_river_flow_data = pd.read_csv('dose_river_flow_data.csv')
kurty_river_flow_data = pd.read_csv('kurty_river_flow_data.csv')

# Шаг 2: Преобразование данных
rainfall_data['date'] = pd.to_datetime(rainfall_data['date'])
dose_river_flow_data['date'] = pd.to_datetime(dose_river_flow_data['date'])
kurty_river_flow_data['date'] = pd.to_datetime(kurty_river_flow_data['date'])

# Шаг 3: Создание модели гидрологического ответа
X_train = rainfall_data[['rainfall']]
y_train = dose_river_flow_data['flow']
model = MLPRegressor()
model.fit(X_train, y_train)

# Шаг 4: Анализ результатов
X_test = kurty_river_flow_data[['rainfall']]
y_pred = model.predict(X_test)
kurty_river_flow_data['predicted_flow'] = y_pred

# Шаг 5: Визуализация результатов
m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

for index, row in rainfall_data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

for index, row in kurty_river_flow_data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=10,
                        color='red',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

m.save("133.html")