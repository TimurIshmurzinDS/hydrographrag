import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Подготовка данных
data = pd.read_csv('tokyraun_river_data.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
lr_model = LinearRegression()
lr_model.fit(train_data[['flow']], train_data['water_demand'])

# Обучение модели случайного леса
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(train_data[['flow']], train_data['water_demand'])

# Прогнозирование потребности в воде для орошения
def predict_water_demand(flow):
    lr_pred = lr_model.predict([[flow]])
    rf_pred = rf_model.predict([[flow]])
    return (lr_pred + rf_pred) / 2

# Визуализация прогнозируемой потребности в воде для орошения на карте бассейна реки Токыраун
m = Map(location=[55.0, 82.0], zoom_start=8)
for i in range(len(data)):
    flow = data['flow'].iloc[i]
    water_demand = predict_water_demand(flow)
    Marker([data['latitude'].iloc[i], data['longitude'].iloc[i]], popup=f'Прогнозируемая потребность в воде для орошения: {water_demand}').add_to(m)

m.save("193.html")